document.addEventListener("DOMContentLoaded", function() {
    const tabs = document.querySelectorAll(".tab");
    const contents = document.querySelectorAll(".content");

    tabs.forEach(tab => {
        tab.addEventListener("click", function() {
            tabs.forEach(t => t.classList.remove("active"));
            contents.forEach(c => c.style.display = "none");

            this.classList.add("active");
            document.getElementById(this.dataset.tab).style.display = "block";
        });
    });

    // Activer le premier onglet par défaut
    tabs[0].classList.add("active");
    contents[0].style.display = "block";

    const showNewCollegeBtn = document.getElementById('showNewCollegeInput');
    const newCollegeGroup = document.getElementById('newCollegeGroup');
    const collegeSelect = document.getElementById('college');
    const newCollegeInput = document.getElementById('newCollege');

    if (showNewCollegeBtn) {
        showNewCollegeBtn.addEventListener('click', function() {
            newCollegeGroup.style.display = 'block';
            showNewCollegeBtn.style.display = 'none';
            collegeSelect.required = false;
            newCollegeInput.required = true;
        });
    }

    if (newCollegeInput) {
        newCollegeInput.addEventListener('input', function() {
            if (this.value) {
                collegeSelect.value = '';
                collegeSelect.disabled = true;
            } else {
                collegeSelect.disabled = false;
                collegeSelect.required = true;
                this.required = false;
            }
        });
    }
});
