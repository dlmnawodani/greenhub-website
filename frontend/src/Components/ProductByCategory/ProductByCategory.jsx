import React, { useState, useEffect, useRef } from "react";
import "../Product/product.css";
import axios from "axios";

//Components
import ProductInfo from "../ProductInfo/ProductInfo";

const ProductByCategory = ({ prod }) => {
  const apiProd = import.meta.env.VITE_API_PROD;
  const overlayRef = useRef(null);

  const [productInfoVisibility, setProductInfoVisibility] = useState(false);
  const [productInfo, setProductInfo] = useState([]);

  const handleProductInfoVisibility = (product) => {
    setProductInfo(product);
    setProductInfoVisibility(true);
  };

  const handleProductInfoCloseClick = () => {
    setProductInfoVisibility(false);
    setProductInfo(null);
  };

  //overlay closes onClick outside the container
  useEffect(() => {
    const handleOutsideClick = (e) => {
      if (overlayRef.current && !overlayRef.current.contains(e.target)) {
        setProductInfoVisibility(false);
      }
    };

    document.addEventListener("mousedown", handleOutsideClick);
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, []);

  return (
    <div className="product__container">
      <div className="product__container-overlay" ref={overlayRef}>
        {productInfoVisibility && (
          <ProductInfo
            productObj={productInfo}
            handleClose={handleProductInfoCloseClick}
          />
        )}
      </div>
      {prod?.map((product) => (
        <div className="product" key={product.id}>
          <div className="product__container-img">
            <img
              src={`${apiProd}/${product.image}`}
              alt=""
              className="productImg"
            />
          </div>
          <div className="product__container-body">
            <div className="product__container-body_details">
              <h3>{product.name}</h3>
              <p>Rs.{product.price}</p>
            </div>
            <div className="product__container-body_cta">
              <button onClick={() => handleProductInfoVisibility(product)}>
                View
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProductByCategory;
