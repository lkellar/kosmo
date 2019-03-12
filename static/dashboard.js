function submitForm(formId) {
    const formData = new FormData( document.getElementById(formId) );
    formData.append('cmd', 'set');
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'control');
    xhr.send(formData);
    return false;
}