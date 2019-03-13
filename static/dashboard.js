function submitForm(formId, cmd='set') {
    const formData = new FormData( document.getElementById(formId) );

    if (cmd === 'set') {
        formData.append('cmd', cmd);
    } else {
        formData.append('cmd', cmd);
        formData.delete('angle');
    }

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'control');
    xhr.onreadystatechange = () => {if (xhr.readyState === 4 && xhr.status === 200) {
        updateAngles(JSON.parse(xhr.response));
    }};
    xhr.send(formData);
    return false;
}

function updateAngles(angles) {

    for (const [key, value] of Object.entries(angles)) {
        for (const [axis, angle] of Object.entries(value)) {
            const angleInput = document.getElementById(`${key}-${axis}-angle`);
            angleInput.value = angle;
        }
    }
}