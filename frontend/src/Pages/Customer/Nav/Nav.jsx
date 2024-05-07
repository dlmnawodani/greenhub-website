import React,{useState} from "react";
import "./nav.css";
import { NavLink, useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { setToken, setUser } from "../../../redux/slices/authSlice";

//imgs
import logo from "../../../assets/images/icons/logo.png";
import search from "../../../assets/images/icons/search.png";
import cart from "../../../assets/images/icons/cart.png";
import profile from "../../../assets/images/icons/profile.png";

const Nav = () => {
  const token = useSelector((state) => state.auth.token);
  const user = useSelector((state) => state.auth.user);
  const dispatch = useDispatch();
  const [isLoading, setIsLoading] = useState(false);
  const apiUrl = import.meta.env.VITE_API_URL;
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(setToken(null));
    dispatch(setUser(null));
    localStorage.removeItem("accessToken");
    localStorage.removeItem("authUser");
    console.log("token rm");
  };
  return (
    <header className="wrapper row align-center">
      <div className="wrapper-left">
        <NavLink to="/">
          <img src={logo} alt="GreenHub" className="logo pointer" />
        </NavLink>
      </div>
      <div className="wrapper-search">
        <input type="search" />
        <img src={search} alt="search" className="icon pointer" />
      </div>
      <div className="wrapper-guest_right row">
        <NavLink to="/">
          <h3 className="pointer">Home</h3>
        </NavLink>
        <img src={cart} alt="cart" className="icon pointer" />
        <img src={profile} alt="profile" className="icon" />
        <NavLink to="/">
          <button className="btn-primary" onClick={handleLogout}>Logout</button>
        </NavLink>
      </div>
    </header>
  );
};

export default Nav;
