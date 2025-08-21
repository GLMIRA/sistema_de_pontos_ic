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
    function applytheme(theme){
        html.setAttribute("data-bs-theme", theme);
        toggleBtn.textContent = theme === "dark"?"☀️":"🌙";
        localStorage.setItem("theme",theme);
        console.log('💾 Tema aplicado: ${theme}');
    }
    let savedtheme = localStorage.getItem("theme");

    if(!savedtheme){
        savedtheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";console.log(`🌍 Tema detectado pelo sistema: ${savedTheme}`);
    }
    applytheme(savedtheme);
    toggleBtn.addEventListener("click", () => {
        const currentTheme = html.getAttribute("data-bs-theme") || "light";
        const newTheme = currentTheme === "light" ? "dark" : "light";
        applytheme(newTheme);
    });
 
});

