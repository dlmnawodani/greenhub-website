import React, { useState } from "react";
import "./dltUser.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";
import { setToken, setUser } from "../../../../redux/slices/authSlice";
import { Toaster, toast } from "react-hot-toast";
import { useNavigate } from "react-router-dom";

const DltUser = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [userId, setUserId] = useState();
  const onSubmitHandler = async (e) => {
    e.preventDefault();
    try {
      const params = new URLSearchParams();
      const response = await axios.delete(`${apiUrl}/users/${userId}`);
      if (response.data) {
        console.log("Dlt success", response.data);
        toast("User Deleted Successfully!🌱");
      }
    } catch (e) {
      console.log("Err", e.message);
      toast("User Deletion Error!🌱");
    }
  };
  return (
    <div className="delete__container">
      <form onSubmit={onSubmitHandler}>
        <input
          type="text"
          placeholder="User Id"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />
        <button type="submit" className="primary-btn">
          Delete
        </button>
      </form>
      <Toaster />
    </div>
  );
};

export default DltUser;
