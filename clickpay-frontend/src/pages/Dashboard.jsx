// src/pages/Dashboard.jsx
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token"); // حذف التوكن
    navigate("/login"); // الرجوع لصفحة تسجيل الدخول
  };

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-blue-600">
          مرحبًا في لوحة التحكم الخاصة بـ Click Pay 🎉
        </h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        >
          تسجيل الخروج
        </button>
      </div>
      <p className="text-gray-700">
        هنا هتتابع كل معاملاتك المالية وتدير نظام الدفع بسهولة.
      </p>
    </div>
  );
}

export default Dashboard;
