import React from 'react';

const ProjectList = ({ projects, onSelectProject, currentProjectId }) => {
  if (!projects || projects.length === 0) {
    return (
      <div className="bg-gray-800 p-4 rounded-lg text-center">
        <p className="text-gray-400">No projects found. Create a new project to get started.</p>
      </div>
    );
  }

  return (
    <div className="projects-list mt-6">
      <h3 className="text-xl font-bold mb-4">Collaborative Projects</h3>
      <div className="grid gap-4">
        {projects.map((project) => {
          const isActive = project.status === "Active";
          const statusColor = isActive ? "text-green-400" : "text-purple-400";
          const isSelected = currentProjectId === project.id;
          
          return (
            <div 
              key={project.id}
              className={`bg-gray-800 p-4 rounded-lg border ${
                isSelected ? 'border-green-400' : 'border-gray-700'
              } hover:border-green-400 transition-all cursor-pointer`}
              onClick={() => onSelectProject(project.id)}
            >
              <div className="flex justify-between items-center">
                <h4 className="text-lg font-bold text-white">{project.name}</h4>
                <div className={`text-sm font-semibold ${statusColor}`}>
                  {project.status}
                </div>
              </div>
              <p className="text-gray-400 my-2">{project.description}</p>
              <div className="flex gap-4 text-sm text-gray-400">
                <div>
                  <span className="text-green-400 font-bold">{project.participants}</span> Participants
                </div>
                <div>
                  <span className="text-green-400 font-bold">{project.milestones}</span> Milestones
                </div>
                <div>
                  Created: {project.created_at}
                </div>
              </div>
              {isSelected && (
                <div className="mt-3 text-center">
                  <span className="bg-green-400 text-gray-900 px-3 py-1 rounded-full text-xs font-bold">
                    Selected
                  </span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ProjectList;