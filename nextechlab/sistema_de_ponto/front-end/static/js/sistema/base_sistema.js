
    document.addEventListener('DOMContentLoaded', function () {
        const cadastroLink = document.getElementById('cadastro-link');
        cadastroLink.addEventListener('click', function (e) {
            e.preventDefault();
            alert('Você já está cadastrado!');
            console.log("'vc' não esta fazendo a sua função direito mas fazer o que !");
            
        });
    });