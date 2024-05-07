import React, { useState, useEffect, useRef } from "react";
import "./dashboard.css";
//Components
import AdminCta from "../../../Components/AdminCta/AdminCta";
import CreateProduct from "../Products/CreateProduct/CreateProduct";
const Dashboard = () => {
  const overlayRef = useRef(null);
  const [prodCreateVisibility, setProdCreateVisibility] = useState(false);
  const handleProdCreateVisibility = () => {
    setProdCreateVisibility(true);
    console.log("trueeeeeee");
  };
  const handleProdCreateClose = () => {
    setProdCreateVisibility(false);
  };
  //overlay closes onClick outside the container
  useEffect(() => {
    const handleOutsideClick = (e) => {
      if (overlayRef.current && !overlayRef.current.contains(e.target)) {
        setProdCreateVisibility(false);
      }
    };

    document.addEventListener("mousedown", handleOutsideClick);
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, []);
  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>
      <div className="overlay-components" ref={overlayRef}>
        {prodCreateVisibility && <CreateProduct />}
      </div>
      <h3>Products</h3>
      <div className="products-cta">
        <button onClick={handleProdCreateVisibility}>
          <AdminCta bgColor={"#39B54A"} ctaName={"Create Product"} />
        </button>
        <button>
          <AdminCta bgColor={"#C23E45"} ctaName={"Delete Product"} />
        </button>
        <button>
          <AdminCta bgColor={"#1A8F93"} ctaName={"All Products"} />
        </button>
      </div>
      <h3>Users</h3>
      <div className="users-cta">
        <button>
          <AdminCta bgColor={"#1A8F93"} ctaName={"All Users"} />{" "}
        </button>
        <button>
          <AdminCta bgColor={"#39B54A"} ctaName={"Most Bought"} />
        </button>
        <button>
          <AdminCta bgColor={"#8B2A48"} ctaName={"Toxic Users"} />
        </button>
        <button>
          <AdminCta bgColor={"#E97F47"} ctaName={"Positive Users"} />
        </button>
        <button>
          <AdminCta bgColor={"#C23E45"} ctaName={"Delete User"} />
        </button>
      </div>
      <h3>Orders</h3>
      <div className="orders-cta">
        <button>
          <AdminCta bgColor={"#1A8F93"} ctaName={"All Orders"} />
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
