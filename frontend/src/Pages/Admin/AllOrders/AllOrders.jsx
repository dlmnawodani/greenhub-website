import React, { useState, useEffect } from "react";
import "./allOrders.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";

const AllOrders = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const user = useSelector((state) => state.auth.user);
  const [isLoading, setIsLoading] = useState(false);
  //get
  const [ordersData, setordersData] = useState(null);
  const loadOrders = async () => {
    try {
      const response = await axios.get(`${apiUrl}/orders`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.data) {
        setordersData(response.data);
        console.log("orders", response.data);
      }
    } catch (error) {
      console.log("err orders", error.message);
    }
  };
  useEffect(() => {
    if (token || !isLoading) {
      (async () => {
        await loadOrders();
        setIsLoading(true);
      })();
    }
  }, [token, isLoading]);
  return (
    <div className="all__container">
      <h3>All Orders</h3>
      {ordersData &&
        ordersData.result.map((p, i) => (
          <div className="prod__details" key={p.id}>
            <h3>{i + 1}</h3>
            <h3>{p.user.first_name+"  "+p.user.last_name}</h3>
            <h3>{p.user.email}</h3>
            <h3>Due: Rs.{p.order_due_amount}</h3>
            <h3>Id:{p.id}</h3>
            <h3>{p.order_status}</h3>
          </div>
        ))}
    </div>
  );
};

export default AllOrders;
