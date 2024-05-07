import React,{useState, useEffect} from "react";
import "./home.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";

// Components
import Product from "../../../Components/Product/Product";

const Home = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const [isLoading, setIsLoading] = useState(false);

  //get
  const [productsData, setProductsData] = useState(null);
  const loadProducts = async () => {
    try {
      const response = await axios.get(`${apiUrl}/products`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.data) {
        setProductsData(response.data);
        console.log("products", response.data);
      }
    } catch (error) {
      console.log("err products", error.message);
    }
  };
  useEffect(() => {
    if (token && !isLoading) {
      (async () => {
        await loadProducts();
        setIsLoading(true);
      })();
    }
  }, [token, isLoading]);

  return (
    <div className="home__container">
      <h1 className="home__container-header">Browse All Products</h1>
      <div className="products__section">
        <Product prod={productsData} />
      </div>
    </div>
  );
};

export default Home;
