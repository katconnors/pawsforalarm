const lookupButton = document.querySelector('#lookup-shelter-button');
const shelterIdDrop = document.querySelector('#shelterid');
const typedField = document.querySelector('#shelter-name');

// updates shelter dropdown menu with shelters from pfa db

lookupButton.addEventListener('click', () => {
    const paramurl = `/sheltername?shelter-name=${typedField.value}`;

    fetch(paramurl)
    
        .then((reply) => reply.json())
        .then((jsonDict) => {
        shelterIdDrop.innerHTML = ``
        const shelter_id_namelist = jsonDict["shelters"]
        for (const entry of shelter_id_namelist)  {
            shelterIdDrop.innerHTML = `${shelterIdDrop.innerHTML}<option value="${entry["id"]}">${entry["name"]} </option>`;
        }
    });

});