function showLoading() {
    const button =
        document.getElementById(
            "generateBtn"
        );

    const loading =
        document.getElementById(
            "loading"
        );

    if (button && loading) {

        button.disabled = true;

        button.textContent =
            "Generating…";

        loading.hidden = false;
    }
}