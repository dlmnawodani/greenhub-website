import React, { useState, useEffect } from "react";
import "./mostBought.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";

const MostBought = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const user = useSelector((state) => state.auth.user);
  const [isLoading, setIsLoading] = useState(false);

  //get
  const [mostSoldData, setMostSoldData] = useState(null);

  const loadMostSold = async () => {
    try {
      const response = await axios.get(
        `${apiUrl}/users-with-most-sold-product`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (response.data) {
        setMostSoldData(response.data);
        console.log("mostSold", response.data);
      }
    } catch (error) {
      console.log("err mostSold", error.message);
    }
  };
  useEffect(() => {
    if (token || !isLoading) {
      (async () => {
        await loadMostSold();
        setIsLoading(true);
      })();
    }
  }, [token, isLoading]);
  return (
    <div className="mostBought__container">
      <h3>Most Bought & Active Users</h3>
      {mostSoldData &&
        mostSoldData.result.slice(0, 3).map((u, i) => (
          <div className="prod__details" key={u.id}>
            <h3>{i + 1}</h3>
            <h3>{u.first_name + "  " + u.last_name}</h3>
            <h3>{u.phone_number}</h3>
            <h3>{u.email}</h3>
            <h3>{u.user_role}</h3>
          </div>
        ))}
    </div>
  );
};

export default MostBought;
