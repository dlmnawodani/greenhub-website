import React, { useState, useEffect } from "react";
import "./cusProfile.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";
import { Toaster, toast } from "react-hot-toast";
import moment from "moment";

const CusProfile = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const user = useSelector((state) => state.auth.user);
  const [isLoading, setIsLoading] = useState(false);

  console.log("user", user);
  //get
  const [ordersData, setOrdersData] = useState(null);
  const loadOrders = async () => {
    try {
      const response = await axios.get(`${apiUrl}/orders?user_id=${user.id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.data) {
        setOrdersData(response.data);
        console.log("orders", response.data);
      }
    } catch (error) {
      console.log("err products", error.message);
    }
  };
  useEffect(() => {
    if (token && !isLoading) {
      (async () => {
        await loadOrders();
        setIsLoading(true);
      })();
    }
  }, [token, isLoading]);
  return (
    <div className="cusProfile__container">
      <h3 className="header__h3">Orders</h3>
      {ordersData &&
        ordersData.result.map((order) => (
          <div className="cusProfile__orders" key={order.id}>
            <h3>{moment(order.created_at).format("DD-MM-YYYY")}</h3>
            <h3>{order.remark}</h3>
            <h3>Rs.{order.order_total_amount}</h3>
            <h3>{order.order_status}</h3>
          </div>
        ))}
        <p>**Don't forget to review our products after the delivery</p>
    </div>
  );
};

export default CusProfile;
