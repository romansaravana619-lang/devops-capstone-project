import React, { useState } from "react";
import "./Register.css";

const Register = () => {
  const [form, setForm] = useState({username:"", firstName:"", lastName:"", email:"", password:""});
  const update = e => setForm({...form,[e.target.name]:e.target.value});
  const submit = async e => {
    e.preventDefault();
    await fetch("/djangoapp/register",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(form)});
  };
  return (
    <div className="register_container">
      <h1 className="header">Sign-up</h1>
      <form className="inputs" onSubmit={submit}>
        <input className="input_field" name="username" placeholder="Username" value={form.username} onChange={update} required />
        <input className="input_field" name="firstName" placeholder="First Name" value={form.firstName} onChange={update} required />
        <input className="input_field" name="lastName" placeholder="Last Name" value={form.lastName} onChange={update} required />
        <input className="input_field" name="email" type="email" placeholder="Email" value={form.email} onChange={update} required />
        <input className="input_field" name="password" type="password" placeholder="Password" value={form.password} onChange={update} required />
        <div className="submit_panel"><button className="submit" type="submit">Register</button></div>
      </form>
    </div>
  );
};
export default Register;
