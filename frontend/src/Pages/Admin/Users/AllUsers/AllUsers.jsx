import React, { useState, useEffect } from "react";
import "./allUsers.css";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";

const AllUsers = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const user = useSelector((state) => state.auth.user);
  const [isLoading, setIsLoading] = useState(false);
  //get
  const [usersData, setUsersData] = useState(null);
  const loadUsers = async () => {
    try {
      const response = await axios.get(`${apiUrl}/users`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.data) {
        setUsersData(response.data);
        console.log("users", response.data);
      }
    } catch (error) {
      console.log("err users", error.message);
    }
  };
  useEffect(() => {
    if (token || !isLoading) {
      (async () => {
        await loadUsers();
        setIsLoading(true);
      })();
    }
  }, [token, isLoading]);
  return (
    <div className="users__container">
      <h3>All Users</h3>
      {usersData &&
        usersData.result.map((u, i) => (
          <div className="prod__details" key={u.id}>
            <h3>{i + 1}</h3>
            <h3>{u.first_name +"  " + u.last_name}</h3>
            <h3>{u.phone_number}</h3>
            <h3>{u.email}</h3>
            <h3>{u.user_role}</h3>
          </div>
        ))}
    </div>
  );
};

export default AllUsers;
