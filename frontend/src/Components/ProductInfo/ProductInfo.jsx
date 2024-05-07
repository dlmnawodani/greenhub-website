import React, { useState } from "react";
import "./productInfo.css";
import axios from "axios";
import toast, { Toaster } from "react-hot-toast";
import { useSelector, useDispatch } from "react-redux";

//imgs
import ecoCertified from "../../assets/images/bgs/eco.jpg";

const ProductInfo = ({ productObj, handleClose }) => {
  const apiProd = import.meta.env.VITE_API_PROD;
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const [isLoading, setIsLoading] = useState(false);
  console.log("prod", productObj);

  const [prodQuantity, setProdQuantity] = useState();

  const addToCart = async (e) => {
    e.preventDefault();
    const config = {
      headers: {
        Authorization: `Bearer ${token}`,
        "content-type": "application/json",
      },
    };
    const data = {
      product_id: productObj.id,
      qty: (prodQuantity > 0 ? prodQuantity : "exception"),
    };
    try {
      const response = await axios.post(`${apiUrl}/carts/items`, data, config);
      toast("Items Added to Cart Successfully!🌱");
    } catch (e) {
      toast("Oops! Select 1 or more🌱");
      console.log(e.message);
    }
  };
  return (
    <div className="productInfo__container">
      <div className="productInfo__container-banner">
        <img src={`${apiProd}/${productObj.image}`} />
      </div>
      <div className="productInfo__container-details">
        <h3>{productObj.name}</h3>
        <p>{productObj.remark}</p>
        <p className="productInfo__price">Price: Rs.{productObj.price}</p>
        <p>
          In-Stock:{" "}
          {productObj.qty_in_stock > 1
            ? productObj.qty_in_stock
            : "Out of Stock"}
        </p>
        <p>Select Quantity : </p>
        <input
          type="number"
          className="productInfo__quantity"
          value={prodQuantity}
          onChange={(e) => setProdQuantity(e.target.value)}
        />

        <div className="cta__btns">
          <button
            type="button"
            className="cta__btns-addCart"
            onClick={addToCart}
          >
            Add to Cart
          </button>
          <button
            type="button"
            onClick={handleClose}
            className="cta__btns-cancel"
          >
            Cancel
          </button>
        </div>
        <div className="productInfo__certified">
          <img src={ecoCertified} alt="Eco Certified" />
        </div>
      </div>
      <Toaster />
    </div>
  );
};

export default ProductInfo;
