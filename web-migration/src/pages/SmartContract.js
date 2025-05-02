import React, { useState, useEffect } from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';

// Component imports
import ContractHeader from '../components/smart-contract/ContractHeader';
import ProjectForm from '../components/smart-contract/ProjectForm';
import ProjectList from '../components/smart-contract/ProjectList';
import ContractExplorer from '../components/smart-contract/ContractExplorer';
import MilestoneSection from '../components/smart-contract/MilestoneSection';
import ParticipantSection from '../components/smart-contract/ParticipantSection';

const SmartContract = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const [currentProjectId, setCurrentProjectId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [projects, setProjects] = useState([]);
  const [milestones, setMilestones] = useState([]);
  const [participants, setParticipants] = useState([]);

  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        // These would be actual API calls in the real implementation
        // For now, we'll use placeholder data similar to what we have in Streamlit
        const projectsResponse = await fetch('/api/projects');
        const projectsData = await projectsResponse.json();
        setProjects(projectsData);

        if (currentProjectId) {
          const milestonesResponse = await fetch(`/api/projects/${currentProjectId}/milestones`);
          const milestonesData = await milestonesResponse.json();
          setMilestones(milestonesData);

          const participantsResponse = await fetch(`/api/projects/${currentProjectId}/participants`);
          const participantsData = await participantsResponse.json();
          setParticipants(participantsData);
        }

        setError(null);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load data. Please try again later.');
        
        // Add fallback data if the API calls fail
        setProjects([
          {
            id: "proj1",
            name: "Quantum Research Collaboration",
            description: "A collaborative project to research quantum computing applications in bioinformatics",
            participants: 3,
            milestones: 2,
            created_at: "2025-04-15",
            status: "Active"
          },
          {
            id: "proj2",
            name: "Decentralized AI Training Framework",
            description: "Developing a framework for decentralized AI model training using blockchain validation",
            participants: 5,
            milestones: 4,
            created_at: "2025-03-28",
            status: "Active"
          }
        ]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [currentProjectId]);

  const handleProjectSelect = (projectId) => {
    setCurrentProjectId(projectId);
  };

  const handleProjectCreate = async (projectData) => {
    try {
      // This would be an actual API call in the real implementation
      const response = await fetch('/api/projects', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(projectData),
      });
      
      if (!response.ok) {
        throw new Error('Failed to create project');
      }
      
      const newProject = await response.json();
      setProjects([newProject, ...projects]);
      setCurrentProjectId(newProject.id);
      
      return { success: true, project: newProject };
    } catch (err) {
      console.error('Error creating project:', err);
      return { success: false, error: err.message };
    }
  };

  return (
    <div className="smart-contract-container">
      <h1 className="text-3xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-purple-500">
        DAPPR Smart Contract
      </h1>
      
      <Tabs selectedIndex={tabIndex} onSelect={index => setTabIndex(index)}>
        <TabList className="flex bg-gray-800 p-2 rounded-lg mb-6">
          <Tab className="px-4 py-2 cursor-pointer rounded transition-all duration-200 mr-2 hover:bg-gray-700 focus:outline-none">Projects</Tab>
          <Tab className="px-4 py-2 cursor-pointer rounded transition-all duration-200 mr-2 hover:bg-gray-700 focus:outline-none">Contract Explorer</Tab>
          <Tab className="px-4 py-2 cursor-pointer rounded transition-all duration-200 mr-2 hover:bg-gray-700 focus:outline-none">Milestones</Tab>
          <Tab className="px-4 py-2 cursor-pointer rounded transition-all duration-200 hover:bg-gray-700 focus:outline-none">Participants</Tab>
        </TabList>

        <TabPanel>
          <div className="mb-6">
            <ContractHeader />
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <ProjectForm onSubmit={handleProjectCreate} />
              </div>
            </div>
            {isLoading ? (
              <div className="flex justify-center py-10">
                <div className="spinner"></div>
              </div>
            ) : error ? (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mt-4">
                {error}
              </div>
            ) : (
              <ProjectList 
                projects={projects} 
                onSelectProject={handleProjectSelect}
                currentProjectId={currentProjectId}
              />
            )}
          </div>
        </TabPanel>

        <TabPanel>
          <ContractExplorer />
        </TabPanel>

        <TabPanel>
          <MilestoneSection 
            projectId={currentProjectId} 
            milestones={milestones}
            isLoading={isLoading}
            error={error}
          />
        </TabPanel>

        <TabPanel>
          <ParticipantSection 
            projectId={currentProjectId}
            participants={participants}
            isLoading={isLoading}
            error={error}
          />
        </TabPanel>
      </Tabs>
    </div>
  );
};

export default SmartContract;