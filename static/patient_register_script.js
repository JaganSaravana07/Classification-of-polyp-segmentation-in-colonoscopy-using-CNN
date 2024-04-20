const recordForm = document.getElementById('record-form');
const idInput = document.getElementById('identity');
const nameInput = document.getElementById('name');
const ageInput = document.getElementById('age');
const emailInput = document.getElementById('email');
const bloodgroupInput = document.getElementById('blood_group');
const addressInput = document.getElementById('address');
const genderInput = document.getElementById('gender');
const mobilenoInput = document.getElementById('mobile');
const editIndexInput = document.getElementById('edit-index');

recordForm.addEventListener('submit', function (e) {
  e.preventDefault();
  const identity = idInput.value;
  const name = nameInput.value;
  const age = ageInput.value;
  const email = emailInput.value;
  const blood_group = bloodgroupInput.value;
  const address = addressInput.value;
  const gender = genderInput.value;
  const mobile = mobilenoInput.value;
  const editIndex = parseInt(editIndexInput.value);

  if (name && age && email) {
    // Construct URL with parameters
    const databaseURL = `patient_details.html?id=${identity}&name=${name}&age=${age}&email=${email}&blood_group=${blood_group}&address=${address}&gender=${gender}&mobile=${mobile}`;

    // Redirect to the patient details page
    window.location.href = "patient_details.html";
  }
});
