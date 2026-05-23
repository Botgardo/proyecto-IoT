function maskPin(pin) {
    return pin ? "•".repeat(pin.length) : "—";
}

function fmtDate(s) {
    const d = new Date(s.replace(" ", "T"));
    return d.toLocaleDateString("es-MX", { day: "2-digit", month: "short", year: "numeric" })
        + " " + d.toLocaleTimeString("es-MX", { hour: "2-digit", minute: "2-digit" });
}

function renderTabla(data) {
    const res = document.getElementById("f-resultado").value;
    const dev = document.getElementById("f-device").value;
    const q   = document.getElementById("f-search").value.toLowerCase();

    const filtered = data.filter(r =>
        (!res || r.resultado === res) &&
        (!dev || r.device_id === dev) &&
        (!q   || r.device_id.toLowerCase().includes(q))
    );

    const tbody = document.getElementById("tabla-body");
    const empty = document.getElementById("tabla-empty");

    if (!filtered.length) {
        tbody.innerHTML = "";
        empty.style.display = "block";
        return;
    }

    empty.style.display = "none";
    tbody.innerHTML = filtered.map(r => `
        <tr>
            <td style="color:#666; font-size:12px;">${r.id}</td>
            <td><span class="device-tag">${r.device_id}</span></td>
            <td style="font-family: monospace; letter-spacing: 2px;">${maskPin(r.pin_ingresado)}</td>
            <td>
                <span class="badge ${r.resultado === 'AUTORIZADO' ? 'badge-ok' : 'badge-fail'}">
                    ${r.resultado === 'AUTORIZADO' ? 'Autorizado' : 'Denegado'}
                </span>
            </td>
            <td style="color:#888; font-size:12px;">${fmtDate(r.fecha_hora)}</td>
        </tr>
    `).join("");
}

async function initDashboard() {
    const response = await fetch("/api/accesos");
    const data = await response.json();

    const total = data.length;
    const ok    = data.filter(r => r.resultado === "AUTORIZADO").length;
    const fail  = total - ok;
    const last  = data[0];

    document.getElementById("m-total").textContent       = total;
    document.getElementById("m-ok").textContent          = ok;
    document.getElementById("m-fail").textContent        = fail;
    document.getElementById("m-ok-pct").textContent      = Math.round(ok / total * 100) + "% del total";
    document.getElementById("m-fail-pct").textContent    = Math.round(fail / total * 100) + "% del total";
    document.getElementById("m-last").textContent        = last ? fmtDate(last.fecha_hora) : "—";
    document.getElementById("m-last-device").textContent = last ? last.device_id : "—";

    const devices = [...new Set(data.map(r => r.device_id))];
    const sel = document.getElementById("f-device");
    devices.forEach(d => {
        const o = document.createElement("option");
        o.value = d;
        o.textContent = d;
        sel.appendChild(o);
    });

    const horas = Array(24).fill(0);
    data.forEach(r => {
        horas[new Date(r.fecha_hora.replace(" ", "T")).getHours()]++;
    });

    new Chart(document.getElementById("chartHora"), {
        type: "bar",
        data: {
            labels: horas.map((_, i) => i % 3 === 0 ? i + "h" : ""),
            datasets: [{
                data: horas,
                backgroundColor: "#185FA5",
                borderRadius: 3,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        title: (i) => i[0].dataIndex + "h",
                        label: (i) => i.raw + " accesos"
                    }
                }
            },
            scales: {
                x: { grid: { display: false }, ticks: { color: "#888", font: { size: 11 } } },
                y: { grid: { color: "rgba(255,255,255,0.06)" }, ticks: { color: "#888", font: { size: 11 }, stepSize: 1 }, beginAtZero: true }
            }
        }
    });

    new Chart(document.getElementById("chartDonut"), {
        type: "doughnut",
        data: {
            labels: ["Autorizados", "Denegados"],
            datasets: [{
                data: [ok, fail],
                backgroundColor: ["#1D9E75", "#E24B4A"],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: false,
            cutout: "68%",
            plugins: {
                legend: { display: false },
                tooltip: { callbacks: { label: (i) => " " + i.label + ": " + i.raw } }
            }
        }
    });

    document.getElementById("donut-legend").innerHTML = `
        <span><span class="legend-dot" style="background:#1D9E75;"></span>Autorizados — ${ok}</span>
        <span><span class="legend-dot" style="background:#E24B4A;"></span>Denegados — ${fail}</span>
    `;

    ["f-resultado", "f-device", "f-search"].forEach(id => {
        document.getElementById(id).addEventListener("input", () => renderTabla(data));
    });

    renderTabla(data);
}

initDashboard();