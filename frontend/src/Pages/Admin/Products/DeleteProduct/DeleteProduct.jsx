import React, { useState } from "react";
import "./deleteProduct.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";
import { setToken, setUser } from "../../../../redux/slices/authSlice";
import { Toaster, toast } from "react-hot-toast";
import { useNavigate } from "react-router-dom";

const DeleteProduct = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [productId, setProductId] = useState("");
  const onSubmitHandler = async (e) => {
    e.preventDefault();
    try {
      const params = new URLSearchParams();
      const response = await axios.delete(`${apiUrl}/products/${productId}`);

      if (response.data) {
        console.log("Dlt success", response.data);
        toast("Product Deleted Successfully!🌱");
      }
    } catch (e) {
      console.log("Err", e.message);
    }
  };
  return (
    <div className="delete__container">
      <form onSubmit={onSubmitHandler}>
        <input
          type="text"
          placeholder="Product Id"
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
        />
        <button type="submit" className="primary-btn">
          Delete
        </button>
      </form>
      <Toaster />
    </div>
  );
};

export default DeleteProduct;
