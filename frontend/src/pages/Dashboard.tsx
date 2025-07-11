import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useTenant } from '../contexts/TenantContext';

interface DashboardStats {
  total_students: number;
  total_faculty: number;
  total_courses: number;
  active_enrollments: number;
}

const Dashboard: React.FC = () => {
  const { currentTenant } = useTenant();
  const [stats, setStats] = useState<DashboardStats>({
    total_students: 0,
    total_faculty: 0,
    total_courses: 0,
    active_enrollments: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      if (!currentTenant) return;
      
      try {
        setLoading(true);
        
        // Fetch various statistics
        const [studentsRes, facultyRes, coursesRes] = await Promise.all([
          axios.get('/api/students/students/'),
          axios.get('/api/faculty/faculty/'),
          axios.get('/api/courses/courses/')
        ]);

        setStats({
          total_students: studentsRes.data.length,
          total_faculty: facultyRes.data.length,
          total_courses: coursesRes.data.length,
          active_enrollments: 0 // TODO: Implement enrollment count
        });
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [currentTenant]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  const statCards = [
    {
      title: 'Total Students',
      value: stats.total_students,
      icon: '👨‍🎓',
      color: 'bg-blue-500'
    },
    {
      title: 'Total Faculty',
      value: stats.total_faculty,
      icon: '👨‍🏫',
      color: 'bg-green-500'
    },
    {
      title: 'Total Courses',
      value: stats.total_courses,
      icon: '📚',
      color: 'bg-purple-500'
    },
    {
      title: 'Active Enrollments',
      value: stats.active_enrollments,
      icon: '📊',
      color: 'bg-yellow-500'
    }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Overview of your university system</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card, index) => (
          <div key={index} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className={`p-3 rounded-full ${card.color} text-white text-2xl`}>
                {card.icon}
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600">{card.title}</p>
                <p className="text-2xl font-semibold text-gray-900">{card.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activities */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activities</h3>
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span className="text-sm text-gray-600">New student registration: John Doe</span>
              <span className="text-xs text-gray-400">2 hours ago</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-600">Course enrollment: Computer Science 101</span>
              <span className="text-xs text-gray-400">4 hours ago</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
              <span className="text-sm text-gray-600">Faculty leave approved: Dr. Smith</span>
              <span className="text-xs text-gray-400">1 day ago</span>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="flex items-center justify-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors">
              <div className="text-center">
                <div className="text-2xl mb-2">➕</div>
                <span className="text-sm font-medium">Add New Student</span>
              </div>
            </button>
            <button className="flex items-center justify-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-green-500 hover:bg-green-50 transition-colors">
              <div className="text-center">
                <div className="text-2xl mb-2">👨‍🏫</div>
                <span className="text-sm font-medium">Add Faculty Member</span>
              </div>
            </button>
            <button className="flex items-center justify-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-purple-500 hover:bg-purple-50 transition-colors">
              <div className="text-center">
                <div className="text-2xl mb-2">📚</div>
                <span className="text-sm font-medium">Create New Course</span>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;