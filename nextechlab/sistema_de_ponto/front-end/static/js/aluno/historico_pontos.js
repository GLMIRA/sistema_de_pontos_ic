(function () {
    const selectDia = document.getElementById("select-dia");
    const totalHorasEl = document.getElementById("total-horas");
    const registrosLista = document.getElementById("registros-lista");

    function limpar() {
        totalHorasEl.textContent = "0h 0m";
        registrosLista.innerHTML = "";
    }

    function renderData(dataKey) {
        if (!dataKey) { limpar(); return; }
        const dadosDiv = document.getElementById("dados-" + dataKey);
        if (!dadosDiv) { limpar(); return; }

        // total (string formatada já disponível)
        const totalSpan = dadosDiv.querySelector(".total");
        const totalStr = totalSpan?.dataset?.totalStr ?? (totalSpan?.dataset?.total ? (parseFloat(totalSpan.dataset.total).toFixed(2) + "h") : "0h 0m");
        totalHorasEl.textContent = totalStr;

        // registros
        registrosLista.innerHTML = "";
        const ul = dadosDiv.querySelector(".registros");
        if (!ul) return;
        const lis = ul.querySelectorAll("li");
        lis.forEach(li => {
            const tipo = li.dataset.tipo ?? "";
            const hora = li.dataset.hora ?? "";
            const item = document.createElement("li");
            item.className = "lista-item";

            // badge
            const badge = document.createElement("span");
            badge.className = "badge " + (tipo === "entrada" ? "badge-success" : (tipo === "saida" ? "badge-danger" : "badge-secondary"));
            badge.textContent = tipo.charAt(0).toUpperCase() + tipo.slice(1);

            const horaSpan = document.createElement("span");
            horaSpan.className = "hora";
            horaSpan.textContent = hora;

            const left = document.createElement("div");
            left.appendChild(badge);

            item.appendChild(left);
            item.appendChild(horaSpan);
            registrosLista.appendChild(item);
        });
    }

    // evento change
    selectDia.addEventListener("change", function () {
        renderData(this.value);
    });

    // ao carregar, seleciona o primeiro (mais recente) disponível
    window.addEventListener("DOMContentLoaded", function () {
        const firstOpt = selectDia.querySelector("option[value]:not([value=''])");
        if (firstOpt) {
            selectDia.value = firstOpt.value;
            renderData(firstOpt.value);
        }
    });
})();
