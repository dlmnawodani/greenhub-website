import React, { useState, useEffect, useRef } from "react";
import "./categories.css";
import { NavLink } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
//Imgs
import menu from "../../assets/images/icons/menu.png";
import zeroWaste from "../../assets/images/icons/zero.png";
import ecoKitchen from "../../assets/images/icons/kitchen.png";
import beauty from "../../assets/images/icons/beauty.png";
import profile from "../../assets/images/icons/profile.png";
import cart from "../../assets/images/icons/cart.png";
//Components
import CusProfile from "../CusProfile/CusProfile";
import Cart from "../Cart/Cart";

const Categories = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const [isLoading, setIsLoading] = useState(false);
  const overlayRef = useRef(null);

  const [cartVisibility, setCartVisibility] = useState(false);
  const [cusProfileVisibility, setCusProfileVisibility] = useState(false);
  const handleCartVisibility = () => {
    setCartVisibility(true);
    console.log("cart visibile");
  };
  const handleCartCloseClick = () => {
    setCartVisibility(false);
  };
  const handleProfileVisibility = () => {
    setCusProfileVisibility(true);
  };
  const handleProfileCloseClick = () => {
    setCusProfileVisibility(false);
  };
  //overlay closes onClick outside the container
  useEffect(() => {
    const handleOutsideClick = (e) => {
      if (overlayRef.current && !overlayRef.current.contains(e.target)) {
        setCartVisibility(false);
        setCusProfileVisibility(false);
      }
    };

    document.addEventListener("mousedown", handleOutsideClick);
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, []);
  return (
    <div className="categories__container">
      <div className="categories__container-categories">
        <div className="categories__header">
          <img src={menu} />
          <h4>Categories</h4>
        </div>
        <div className="categories__content">
          <ul>
            <NavLink to="/zero-waste">
              <li>
                <img src={zeroWaste} />
                <h4>Zero Waste</h4>
              </li>
            </NavLink>
            <NavLink to="/eco-kitchen">
              <li>
                <img src={ecoKitchen} />
                <h4>Eco Kitchen</h4>
              </li>
            </NavLink>
            <NavLink to="/natural-beauty">
              <li>
                <img src={beauty} />
                <h4>Natural Beauty</h4>
              </li>
            </NavLink>
          </ul>
          <div className="overlay__cta-btns">
            <button className="btn-cta" onClick={handleCartVisibility}>
              <img src={cart} alt="cart" className="icon pointer" />
              <p>Cart</p>
            </button>
            <button className="btn-cta" onClick={handleProfileVisibility}>
              <img src={profile} alt="profile" className="icon" />
              <p>Profile</p>
            </button>
          </div>
        </div>
      </div>
      <div className="overlay__visibility" ref={overlayRef}>
        {cartVisibility && <Cart onClose={handleCartCloseClick} />}
        {cusProfileVisibility && <CusProfile />}
      </div>
    </div>
  );
};

export default Categories;
