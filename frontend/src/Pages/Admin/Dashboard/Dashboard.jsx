import React from "react";
import "./dashboard.css";
//Components
import AdminCta from "../../../Components/AdminCta/AdminCta";
const Dashboard = () => {
  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>
      <h3>Products</h3>
      <div className="products-cta">
        <AdminCta bgColor={"#39B54A"} ctaName={"Create Product"} />
        <AdminCta bgColor={"#C23E45"} ctaName={"Delete Product"} />
        <AdminCta bgColor={"#1A8F93"} ctaName={"All Products"} />
      </div>
      <h3>Users</h3>
      <div className="users-cta">
        <AdminCta bgColor={"#1A8F93"} ctaName={"All Users"} />
        <AdminCta bgColor={"#39B54A"} ctaName={"Most Bought"} />
        <AdminCta bgColor={"#1A8F93"} ctaName={"Toxic Activity"} />
        <AdminCta bgColor={"#1A8F93"} ctaName={"Positive Activity"} />
        <AdminCta bgColor={"#C23E45"} ctaName={"Delete User"} />
      </div>
      <h3>Orders</h3>
      <div className="orders-cta">
        <AdminCta bgColor={"#1A8F93"} ctaName={"All Orders"} />
      </div>
    </div>
  );
};

export default Dashboard;
