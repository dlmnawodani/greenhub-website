import React from "react";
import "./guestNav.css";
import { NavLink } from "react-router-dom";

//imgs
import logo from "../../assets/images/icons/logo.png";
import search from "../../assets/images/icons/search.png";
import cart from "../../assets/images/icons/cart.png";
import profile from "../../assets/images/icons/profile.png";

const GuestNav = () => {
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
      <div className="wrapper-right row">
        <NavLink to="/">
          <h3 className="pointer">Home</h3>
        </NavLink>
        {/* <img
          src={cart}
          alt="cart"
          className="icon pointer"
        />
        <img
          src={profile}
          alt="profile"
          className="icon"
        /> */}
        <NavLink to="/login">
          <button className="btn-primary">Login</button>
        </NavLink>
        <NavLink to="/signup">
          <button className="btn-secondary ml-15">Sign Up</button>
        </NavLink>
      </div>
    </header>
  );
};

export default GuestNav;
