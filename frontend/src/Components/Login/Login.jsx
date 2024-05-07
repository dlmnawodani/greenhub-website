import React, { useState } from "react";
import "./login.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";
import { setToken, setUser } from "../../redux/slices/authSlice";
import { useNavigate } from "react-router-dom";

//imgs
import loginImg from "../../assets/images/bgs/login.png";

const Login = () => {
  const [userMail, setUserMail] = useState("");
  const [userPassword, setUserPassword] = useState("");

  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const onSubmitHandler = async (e) => {
    e.preventDefault();
    try {
      const params = new URLSearchParams();
      params.append("username", userMail);
      params.append("password", userPassword);
      const response = await axios.post(`${apiUrl}/login`, params);
      const token = response.data.access_token;
      if (token) {
        const user = await axios.post(`${apiUrl}/test-token`, null, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        dispatch(setToken(token));
        dispatch(setUser(user.data));
        console.log("auth success", response.data);
        if (user) {
          navigate("/");
        }
      }
    } catch (e) {
      console.log("Err", e.message);
    }
  };

  return (
    <div className="wrapper row">
      <div className="wrapper-left">
        <img src={loginImg} />
        <h3 className="primary-text">
          WELCOME TO <span>GREENHUB</span>
        </h3>
        <p>
          Our eco-friendly digital haven, where sustainable living meets
          effortless shopping!
        </p>
      </div>
      <div className="wrapper-right">
        <form onSubmit={onSubmitHandler}>
          <label>
            <p>Your Email</p>
            <input
              type="email"
              id="username"
              name="username"
              value={userMail}
              onChange={(e) => setUserMail(e.target.value)}
              required
            />
          </label>
          <label>
            <p>Password</p>
            <input
              type="password"
              className="input-password"
              id="password"
              name="password"
              value={userPassword}
              onChange={(e) => setUserPassword(e.target.value)}
              required
            />
          </label>
          <button type="submit" className="btn-login">
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
