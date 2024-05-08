import React, { useState, useEffect, useRef } from "react";
import "./dashboard.css";
//Components
import AdminCta from "../../../Components/AdminCta/AdminCta";
import CreateProduct from "../Products/CreateProduct/CreateProduct";
import DeleteProduct from "../Products/DeleteProduct/DeleteProduct";
import AllProducts from "../Products/AllProducts/AllProducts";
import AllUsers from "../Users/AllUsers/AllUsers";
import MostBought from "../Users/MostBought/MostBought";
import Toxic from "../Users/Toxic/Toxic";
import DltUser from "../Users/DltUser/DltUser";
import AllOrders from "../AllOrders/AllOrders";
const Dashboard = () => {
  const overlayRef = useRef(null);
  const [prodCreateVisibility, setProdCreateVisibility] = useState(false);
  const [prodDltVisibility, setProdDltVisibility] = useState(false);
  const [productsVisibility, setProductsVisibility] = useState(false);
  //Note- went without visibility in name. all the below states and funcs are of visibility
  const [usersVisi, setUsersVisi] = useState(false);
  const [mostBought, setMostBought] = useState(false);
  const [toxicVisi, setToxicVisi] = useState(false);
  const [dltUser, setDltUser] = useState(false);
  const [ordersVisi, setOrdersVisi] = useState(false);

  const handleProdCreateVisibility = () => {
    setProdCreateVisibility(true);
    console.log("trueeeeeee");
  };
  const handleProdCreateClose = () => {
    setProdCreateVisibility(false);
  };
  const handleProdDltVisi = () => {
    setProdDltVisibility(true);
  };
  const handleProdDltClose = () => {
    setProdDltVisibility(false);
  };

  const handleProductsVisibility = () => {
    setProductsVisibility(true);
  };
  const handleProductsClose = () => {
    setProductsVisibility(false);
  };

  const handleUsersVisi = () => {
    setUsersVisi(true);
  };
  const handleUsersClose = () => {
    setUsersVisi(false);
  };

  const handlemostBought = () => {
    setMostBought(true);
  };
  const handleMostBoughtClose = () => {
    setMostBought(false);
  };
  const handleToxicVisi = () => {
    setToxicVisi(true);
  };
  const handleToxicClose = () => {
    setToxicVisi(false);
  };
  const handleDltUser = () => {
    setDltUser(true);
  }
  const handleDltUserClose = () => {
    setDltUser(false);
  }
  const handleOrdersvisi = () => {
    setOrdersVisi(true)
  }
  const handleOrdersClose = () => {
    setOrdersVisi(false)
  }


  //overlay closes onClick outside the container
  useEffect(() => {
    const handleOutsideClick = (e) => {
      if (overlayRef.current && !overlayRef.current.contains(e.target)) {
        setProdCreateVisibility(false);
        setProdDltVisibility(false);
        setProductsVisibility(false);
        setUsersVisi(false);
        setMostBought(false);
        setToxicVisi(false);
        setDltUser(false);
        setOrdersVisi(false);
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
        {prodDltVisibility && <DeleteProduct />}
        {productsVisibility && <AllProducts />}
        {usersVisi && <AllUsers />}
        {mostBought && <MostBought />}
        {toxicVisi && <Toxic />}
        {dltUser && <DltUser />}
        {ordersVisi && <AllOrders />}
      </div>
      <h3>Products</h3>
      <div className="products-cta">
        <button onClick={handleProdCreateVisibility}>
          <AdminCta bgColor={"#39B54A"} ctaName={"Create Product"} />
        </button>
        <button onClick={handleProdDltVisi}>
          <AdminCta bgColor={"#C23E45"} ctaName={"Delete Product"} />
        </button>
        <button onClick={handleProductsVisibility}>
          <AdminCta bgColor={"#1A8F93"} ctaName={"All Products"} />
        </button>
      </div>
      <h3>Users</h3>
      <div className="users-cta">
        <button onClick={handleUsersVisi}>
          <AdminCta bgColor={"#1A8F93"} ctaName={"All Users"} />{" "}
        </button>
        <button onClick={handlemostBought}>
          <AdminCta bgColor={"#39B54A"} ctaName={"Most Bought"} />
        </button>
        <button onClick={handleToxicVisi}>
          <AdminCta bgColor={"#8B2A48"} ctaName={"Toxic Users"} />
        </button>

        <button onClick={handleDltUser}>
          <AdminCta bgColor={"#C23E45"} ctaName={"Delete User"} />
        </button>
      </div>
      <h3>Orders</h3>
      <div className="orders-cta">
        <button onClick={handleOrdersvisi}>
          <AdminCta bgColor={"#1A8F93"} ctaName={"All Orders"} />
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
