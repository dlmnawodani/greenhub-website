import React, { useState, useEffect } from "react";
import "./home.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";
import { NavLink } from "react-router-dom";

// Components
import Product from "../../../Components/Product/Product";

//Imgs
import menu from "../../../assets/images/icons/menu.png";
import zeroWaste from "../../../assets/images/icons/zero.png";
import ecoKitchen from "../../../assets/images/icons/kitchen.png";
import beauty from "../../../assets/images/icons/beauty.png";

const Home = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const [isLoading, setIsLoading] = useState(false);

  //get
  const [productsData, setProductsData] = useState(null);



  const loadProducts = async () => {
    try {
      const response = await axios.get(`${apiUrl}/products`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.data) {
        setProductsData(response.data);
        console.log("products", response.data);
      }
    } catch (error) {
      console.log("err products", error.message);
    }
  };
  useEffect(() => {
    if (token && !isLoading) {
      (async () => {
        await loadProducts();
        setIsLoading(true);
      })();
    }
  }, [token, isLoading]);

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
        </div>
      </div>
      <div className="home__products">
        <h1 className="home__container-header">Browse All Products</h1>
        <div className="products__section">
          <Product prod={productsData} />
        </div>
      </div>
    </div>
  );
};

export default Home;
