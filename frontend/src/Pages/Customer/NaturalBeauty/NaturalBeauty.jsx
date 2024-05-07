import React, { useState, useEffect } from "react";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";
import "./naturalBeauty.css";
//Components
import Product from "../../../Components/Product/Product";
import ProductByCategory from "../../../Components/ProductByCategory/ProductByCategory";
import Categories from "../../../Components/Categories/Categories";

const NaturalBeauty = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const [isLoading, setIsLoading] = useState(false);
  //get
  const [productsData, setProductsData] = useState([]);

  const loadProducts = async () => {
    try {
      const response = await axios.get(`${apiUrl}/products`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.data) {
        const filteredProducts = response.data.result.filter(
          (product) =>
            product.category &&
            product.category.id === "6637d0c29129066ed0455c0d"
        );
        setProductsData(filteredProducts);
        console.log("filtered products", filteredProducts);
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
    <div className="naturalBeauty__container">
      <Categories />
      <div className="naturalBeauty__products">
        <h1 className="naturalBeauty__container-header">
          🌼Browse Natural Beauty Products
        </h1>
        <div className="products__section">
          <ProductByCategory prod={productsData} />
        </div>
      </div>
    </div>
  );
};

export default NaturalBeauty;
