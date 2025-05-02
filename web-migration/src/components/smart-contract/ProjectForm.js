import React, { useState } from 'react';

const ProjectForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    ip_terms: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    setSuccess(null);

    try {
      // Validate form data
      if (!formData.name.trim()) {
        throw new Error('Project name is required');
      }

      if (!formData.description.trim()) {
        throw new Error('Project description is required');
      }

      // Submit form data
      const result = await onSubmit(formData);
      
      if (result.success) {
        setSuccess('Project created successfully!');
        // Reset form
        setFormData({
          name: '',
          description: '',
          ip_terms: ''
        });
      } else {
        throw new Error(result.error || 'Failed to create project');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="project-form bg-gray-800 p-5 rounded-lg border-l-4 border-green-400 mb-6">
      <h3 className="text-xl font-bold mb-4">Create New Project</h3>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          {success}
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-400 mb-2" htmlFor="name">
            Project Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 focus:outline-none focus:border-green-400 text-white"
            placeholder="Enter project name"
            disabled={isSubmitting}
          />
        </div>
        
        <div className="mb-4">
          <label className="block text-gray-400 mb-2" htmlFor="description">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 focus:outline-none focus:border-green-400 text-white h-24"
            placeholder="Enter project description"
            disabled={isSubmitting}
          ></textarea>
        </div>
        
        <div className="mb-4">
          <label className="block text-gray-400 mb-2" htmlFor="ip_terms">
            IP Terms (Optional)
          </label>
          <textarea
            id="ip_terms"
            name="ip_terms"
            value={formData.ip_terms}
            onChange={handleChange}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 focus:outline-none focus:border-green-400 text-white h-24"
            placeholder="Enter IP terms for this collaboration"
            disabled={isSubmitting}
          ></textarea>
        </div>
        
        <div className="text-right">
          <button
            type="submit"
            className={`px-6 py-2 rounded bg-gradient-to-r from-green-400 to-purple-500 text-white font-semibold hover:opacity-90 transition-all ${
              isSubmitting ? 'opacity-50 cursor-not-allowed' : ''
            }`}
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Creating...' : 'Create Project'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ProjectForm;