import React, { useState, useEffect } from "react";
import "./allProducts.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";

const AllProducts = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const user = useSelector((state) => state.auth.user);
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
    if (token || !isLoading) {
      (async () => {
        await loadProducts();
        setIsLoading(true);
      })();
    }
  }, [token, isLoading]);
  return <div className="prod__container">
    <h3>All Products</h3>
    {
        productsData && productsData.result.map((p,i) => (
            <div className="prod__details" key={p.id}>
                <h3>{i+1}</h3>
                <h3>{p.name}</h3>
                <h3>Rs.{p.price}</h3>
                <h3>X{p.qty_in_stock}</h3>
            </div>
        ))
    }
  </div>;
};

export default AllProducts;
