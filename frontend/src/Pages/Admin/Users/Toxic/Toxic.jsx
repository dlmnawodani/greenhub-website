import React, { useState, useEffect } from "react";
import "./toxic.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";

const Toxic = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const user = useSelector((state) => state.auth.user);
  const [isLoading, setIsLoading] = useState(false);

  //get
  const [toxicData, setToxicData] = useState(null);

  const loadToxicData = async () => {
    try {
      const response = await axios.get(
        `${apiUrl}/reviews`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (response.data) {
        setToxicData(response.data);
        console.log("tox", response.data);
      } 
    } catch (error) {
      console.log("err tox", error.message);
    }
  };
  useEffect(() => {
    if (token || !isLoading) {
      (async () => {
        await loadToxicData();
        setIsLoading(true);
      })();
    }
  }, [token, isLoading]);
  return (
    <div className="toxic__container">
      <h3>Users with toxic activity</h3>
      {toxicData &&
        toxicData.result.map((u, i) => (
          <div className="prod__details" key={u.id}>
            <h3>{i + 1}</h3>
            <h3>{u.user.first_name + "  " + u.user.last_name}</h3>
            <h3>{u.comment}</h3>
            {/* Note - only trained with 4000+ datasets. need to train with more data for better accuracy. */}
          </div>
        ))}
    </div>
  );
};

export default Toxic;
