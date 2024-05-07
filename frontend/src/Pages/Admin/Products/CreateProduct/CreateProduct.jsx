import React, { useState } from "react";
import "./createProduct.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";
import { setToken, setUser } from "../../../../redux/slices/authSlice";
import { Toaster, toast } from "react-hot-toast";
import { useNavigate } from "react-router-dom";

const CreateProduct = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [category, setCategory] = useState();
  const [imgStr, setImgStr] = useState("");
  const [name, setName] = useState("");
  const [price, setPrice] = useState();
  const [qty, setQty] = useState();
  const [remarks, setRemarks] = useState("");

  const createProduct = async (e) => {
    e.preventDefault();
    const config = {
      headers: {
        Authorization: `Bearer ${token}`,
        "content-type": "application/json",
      },
    };
    const data = {
      category_id: category,
      image: {
        content: imgStr,
        filename: "str",
      },
      name: name,
      price: price,
      qty_in_stock: qty,
      remark: remarks,
    };
    try {
      const response = await axios.post(`${apiUrl}/products`, data, config);
      toast("Product Created Successfully!🌱");
    } catch (e) {
      toast("Oops! Fill all the fields🌱");
      console.log(e.message);
    }
  };

  return (
    <div className="create__container">
      <h1>Create New Product</h1>
      <form onSubmit={createProduct}>
        <input
          type="text"
          placeholder="Category Id"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />
        <input
          type="text"
          placeholder="Image - Base64"
          value={imgStr}
          onChange={(e) => setImgStr(e.target.value)}
        />
        <input
          type="text"
          placeholder="Product Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="number"
          placeholder="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
        />
        <input
          type="number"
          placeholder="Quantity"
          value={qty}
          onChange={(e) => setQty(e.target.value)}
        />
        <input
          type="text"
          placeholder="Remarks"
          value={remarks}
          onChange={(e) => setRemarks(e.target.value)}
        />
        <button type="submit">Create</button>
      </form>
      <Toaster />
    </div>
  );
};

export default CreateProduct;
