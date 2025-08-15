// theme-toggle.js

document.addEventListener("DOMContentLoaded", () => {
    console.log('🎯 Theme toggle script iniciado');

    const html = document.documentElement;
    const toggleBtn = document.getElementById("theme-toggle");

    if (!toggleBtn) {
        console.error('❌ Botão theme-toggle não encontrado!');
        return;
    }

    console.log('✅ Botão theme-toggle encontrado');

    toggleBtn.addEventListener("click", () => {

        const currentTheme = html.getAttribute("data-bs-theme");

        if (currentTheme === "light") {
            html.setAttribute("data-bs-theme", "dark");
            toggleBtn.textContent = "☀️";
        } else {
            html.setAttribute("data-bs-theme", "light");
            toggleBtn.textContent = "🌙";
        }
    });
});