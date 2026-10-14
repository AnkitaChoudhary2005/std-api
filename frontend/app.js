p · JS
// Change this if your FastAPI server runs somewhere else
const API_URL = "http://127.0.0.1:8000/students";
 
let students = [];
 
const $ = (id) => document.getElementById(id);
const form = $("studentForm");
 
// ---------- Helpers ----------
function toast(message, isError = false) {
  const el = $("toast");
  el.textContent = message;
  el.classList.toggle("error", isError);
  el.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => el.classList.remove("show"), 2800);
}
 
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
 
// FastAPI errors come back as {detail: "..."} or {detail: [{msg: "..."}]}
async function request(path, options = {}) {
  const res = await fetch(API_URL + path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const detail = data.detail;
    const message = Array.isArray(detail)
      ? detail.map((d) => d.msg).join(", ")
      : detail || "Something went wrong";
    throw new Error(message);
  }
  return data;
}
 
// ---------- READ: GET /students/ ----------
async function loadStudents() {
  try {
    students = await request("/");
    render();
  } catch (err) {
    toast("Could not load students: " + err.message, true);
  }
}
 
// ---------- Render ----------
function render() {
  const term = $("search").value.trim().toLowerCase();
  const visible = students.filter((s) => s.name.toLowerCase().includes(term));
 
  $("tableBody").innerHTML = visible
    .map(
      (s) => `
      <tr>
        <td>${s.id}</td>
        <td>${escapeHtml(s.name)}</td>
        <td>${s.age}</td>
        <td class="right">
          <button class="btn small" data-edit="${s.id}">Edit</button>
          <button class="btn small danger" data-delete="${s.id}">Delete</button>
        </td>
      </tr>`
    )
    .join("");
  $("emptyMsg").hidden = visible.length > 0;
 
  // Stats
  const ages = students.map((s) => s.age);
  $("statTotal").textContent = students.length;
  $("statAvg").textContent = ages.length
    ? (ages.reduce((a, b) => a + b, 0) / ages.length).toFixed(1)
    : "–";
  $("statMin").textContent = ages.length ? Math.min(...ages) : "–";
  $("statMax").textContent = ages.length ? Math.max(...ages) : "–";
  $("headerCount").textContent = `${students.length} Students Registered`;
  $("footerCount").textContent = `Total: ${students.length}`;
}
 
// ---------- Form modes ----------
function resetForm() {
  form.reset();
  $("studentId").value = "";
  $("formError").textContent = "";
  $("formTitle").textContent = "Add New Student";
  $("formSub").textContent = "Register a new student";
  $("submitBtn").textContent = "Add Student";
  $("cancelBtn").hidden = true;
}
 
function startEdit(id) {
  const s = students.find((x) => x.id === id);
  if (!s) return;
  $("studentId").value = s.id;
  $("name").value = s.name;
  $("age").value = s.age;
  $("formTitle").textContent = "Edit Student";
  $("formSub").textContent = `Updating student #${s.id}`;
  $("submitBtn").textContent = "Update Student";
  $("cancelBtn").hidden = false;
  $("name").focus();
}
 
// ---------- CREATE (POST) / UPDATE (PUT) ----------
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = $("name").value.trim();
  const age = parseInt($("age").value, 10);
  const id = $("studentId").value;
 
  if (!name || name.length > 100) {
    $("formError").textContent = "Name must be 1–100 characters.";
    return;
  }
  if (!Number.isInteger(age) || age <= 0) {
    $("formError").textContent = "Age must be a number greater than 0.";
    return;
  }
  $("formError").textContent = "";
 
  try {
    if (id) {
      await request(`/${id}`, { method: "PUT", body: JSON.stringify({ name, age }) });
      toast("Student updated");
    } else {
      await request("/", { method: "POST", body: JSON.stringify({ name, age }) });
      toast("Student added");
    }
    resetForm();
    await loadStudents();
  } catch (err) {
    $("formError").textContent = err.message;
  }
});
 
$("cancelBtn").addEventListener("click", resetForm);
$("search").addEventListener("input", render);
 
// ---------- Edit / DELETE buttons (event delegation) ----------
$("tableBody").addEventListener("click", async (e) => {
  const editId = e.target.dataset.edit;
  const deleteId = e.target.dataset.delete;
 
  if (editId) startEdit(Number(editId));
 
  if (deleteId && confirm("Delete this student?")) {
    try {
      await request(`/${deleteId}`, { method: "DELETE" });
      toast("Student deleted");
      if ($("studentId").value === deleteId) resetForm();
      await loadStudents();
    } catch (err) {
      toast(err.message, true);
    }
  }
});
 
loadStudents();
