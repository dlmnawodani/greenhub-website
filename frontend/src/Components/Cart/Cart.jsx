import React, { useState, useEffect } from "react";
import "./cart.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";
import { Toaster, toast } from "react-hot-toast";

const Cart = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const [isLoading, setIsLoading] = useState(false);

  //get
  const [cartData, setCartData] = useState(null);
  const loadCart = async () => {
    try {
      const response = await axios.get(`${apiUrl}/carts/items`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.data) {
        setCartData(response.data);
        console.log("cart", response.data);
      }
    } catch (error) {
      console.log("err products", error.message);
    }
  };

  const orderProducts = async (e) => {
    e.preventDefault();
    const config = {
      headers: {
        Authorization: `Bearer ${token}`,
        "content-type": "application/json",
      },
    };
    const data = {
        remark: "New Order"
    };
    try {
      const response = await axios.post(`${apiUrl}/orders`, data, config);
      toast("Order Request Sent Successfully!🌱");
    } catch (e) {
      toast("Oops! Try Again Later🌱");
      console.log(e.message);
    }
  };

  useEffect(() => {
    if (token && !isLoading) {
      (async () => {
        await loadCart();
        setIsLoading(true);
      })();
    }
  }, [token, isLoading]);

  return (
    <div className="cart__container">
      {cartData &&
        cartData.result.map((item, i) => (
          <div className="cart__item" key={item.id}>
            <h3>{i+1}</h3>
            <h3>{item.product.name}</h3>
            <h3>X{item.qty}</h3>
            <h3>Rs.{item.qty * item.product.price}</h3>
            
          </div>
        ))}
        <button type="button" onClick={orderProducts}>Buy Now</button>
        <Toaster />
    </div>
  );
};

export default Cart;
