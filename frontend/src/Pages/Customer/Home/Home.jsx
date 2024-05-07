import React, { useState, useEffect, useRef } from "react";
import "./home.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";
import { NavLink } from "react-router-dom";

// Components
import Product from "../../../Components/Product/Product";
import Cart from "../../../Components/Cart/Cart";
import CusProfile from "../../../Components/CusProfile/CusProfile";

//Imgs
import menu from "../../../assets/images/icons/menu.png";
import zeroWaste from "../../../assets/images/icons/zero.png";
import ecoKitchen from "../../../assets/images/icons/kitchen.png";
import beauty from "../../../assets/images/icons/beauty.png";
import profile from "../../../assets/images/icons/profile.png";
import cart from "../../../assets/images/icons/cart.png";
import ProductByCategory from "../../../Components/ProductByCategory/ProductByCategory";

const Home = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const user = useSelector((state) => state.auth.user);
  const userId = useSelector((state) => state.auth.user.id);
  console.log("us", userId);
  const [isLoading, setIsLoading] = useState(false);
  const overlayRef = useRef(null);
  //get
  const [productsData, setProductsData] = useState(null);
  const [zeroWasteData, setZeroWasteData] = useState(null);
  const [greenKitchenData, setGreenKitchenData] = useState(null);
  const [beautyData, setBeautyData] = useState(null);
  const [mostSoldData, setMostSoldData] = useState(null);
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

  const loadProducts = async () => {
    try {
      const response = await axios.get(`${apiUrl}/products`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.data) {
        setProductsData(response.data);
        console.log("products", response.data);
        const filteredZeroWaste = response.data.result.filter(
          (product) =>
            product.category &&
            product.category.id === "6637d0d69129066ed0455c0e"
        );
        setZeroWasteData(filteredZeroWaste);
        console.log("zeroWaste", filteredZeroWaste);
        const filteredKitchen = response.data.result.filter(
          (product) =>
            product.category &&
            product.category.id === "6637d0dc9129066ed0455c0f"
        );
        setGreenKitchenData(filteredKitchen);
        console.log("kitchen", filteredKitchen);
        const filteredBeauty = response.data.result.filter(
          (product) =>
            product.category &&
            product.category.id === "6637d0c29129066ed0455c0d"
        );
        setBeautyData(filteredBeauty);
        console.log("beauty", filteredBeauty);
      }
    } catch (error) {
      console.log("err products", error.message);
    }
  };
  const loadMostSold = async (userId) => {
    try {
      const response = await axios.get(
        `${apiUrl}/users-with-most-sold-product`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (response.data) {
        const userMostSoldData = response.data.result.find(
          (user) => user.id === userId
        );
        if (userMostSoldData) {
          setMostSoldData(userMostSoldData);
          console.log("mostSold", userMostSoldData);
        } else {
          setMostSoldData(null); // No most sold data found for the current user
          console.log("No most sold data found for the user");
        }
      }
    } catch (error) {
      console.log("err mostSold", error.message);
    }
  };
  useEffect(() => {
    if (token && !isLoading) {
      (async () => {
        await loadProducts();
        await loadMostSold(userId);
        setIsLoading(true);
      })();
    }
  }, [token, isLoading]);
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
    <div className="home__container">
      <div className="home__container-categories">
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
      <div className="home__products">
        <div className="overlay__visibility" ref={overlayRef}>
          {cartVisibility && <Cart />}
          {cusProfileVisibility && <CusProfile />}
        </div>
        <div className="recommended__products">
          <h1 className="home__container-header">Recommended Products</h1>
          {mostSoldData?.most_purchased_product?.category.id ==
          "6637d0d69129066ed0455c0e" ? (
            <div className="products__section">
              <ProductByCategory prod={zeroWasteData} />
            </div>
          ) : mostSoldData?.most_purchased_product?.category.id ==
            "6637d0c29129066ed0455c0d" ? (
            <div className="products__section">
              <ProductByCategory prod={beautyData} />
            </div>
          ) : (
            <div className="products__section">
              <ProductByCategory prod={greenKitchenData} />
            </div>
          )}
        </div>
        <h1 className="home__container-header">Browse All Products</h1>
        <div className="products__section">
          <Product prod={productsData} />
        </div>
      </div>
    </div>
  );
};

export default Home;
