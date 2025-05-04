import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, TouchableOpacity, ActivityIndicator, RefreshControl } from 'react-native';
import { Text, Card, Button, useTheme, Divider, TextInput, Menu } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { useWallet } from '../context/WalletContext';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { Connection, clusterApiUrl } from '@solana/web3.js';
import { getProjects, getMilestones } from '../services/solana-service';

// Tab navigation component
const TabBar = ({ tabs, activeTab, onTabChange }: any) => {
  const theme = useTheme();
  
  return (
    <View style={styles.tabBar}>
      {tabs.map((tab: string, index: number) => (
        <TouchableOpacity
          key={index}
          style={[
            styles.tab,
            activeTab === index && { 
              backgroundColor: theme.colors.primary,
              borderColor: theme.colors.primary,
            }
          ]}
          onPress={() => onTabChange(index)}
        >
          <Text 
            style={[
              styles.tabText,
              activeTab === index && { color: '#000', fontWeight: 'bold' }
            ]}
          >
            {tab}
          </Text>
        </TouchableOpacity>
      ))}
    </View>
  );
};

// Contract Function Component
const ContractFunction = ({ name, description, onPress }: any) => {
  const theme = useTheme();
  
  return (
    <TouchableOpacity 
      style={[styles.contractFunction, { borderLeftColor: theme.colors.primary }]}
      onPress={onPress}
    >
      <Text style={[styles.functionName, { color: theme.colors.primary }]}>{name}</Text>
      <Text style={styles.functionDescription}>{description}</Text>
      <View style={styles.functionAction}>
        <Text style={{ color: theme.colors.primary, fontSize: 12 }}>View on Explorer</Text>
        <Icon name="open-in-new" size={12} color={theme.colors.primary} style={{ marginLeft: 4 }} />
      </View>
    </TouchableOpacity>
  );
};

// Contract Event Component
const ContractEvent = ({ name, time, transaction, onPress }: any) => {
  const theme = useTheme();
  
  return (
    <TouchableOpacity 
      style={[styles.contractEvent, { borderLeftColor: theme.colors.accent }]}
      onPress={onPress}
    >
      <View style={styles.eventHeader}>
        <Text style={[styles.eventName, { color: theme.colors.accent }]}>{name}</Text>
        <Text style={styles.eventTime}>{time}</Text>
      </View>
      <Text style={styles.eventTransaction}>TX: {transaction}</Text>
      <View style={styles.eventAction}>
        <Text style={{ color: theme.colors.accent, fontSize: 12 }}>View Transaction</Text>
        <Icon name="open-in-new" size={12} color={theme.colors.accent} style={{ marginLeft: 4 }} />
      </View>
    </TouchableOpacity>
  );
};

// Project Card Component
const ProjectCard = ({ project, isSelected, onSelect, onDetails }: any) => {
  const theme = useTheme();
  const isActive = project.status === "Active";
  const statusColor = isActive ? theme.colors.primary : theme.colors.accent;
  
  return (
    <TouchableOpacity 
      style={[
        styles.projectCard, 
        { 
          backgroundColor: theme.colors.surface,
          borderColor: isSelected ? theme.colors.primary : 'transparent',
        }
      ]}
      onPress={() => onSelect(project.id)}
    >
      <View style={styles.projectHeader}>
        <Text style={styles.projectTitle}>{project.name}</Text>
        <Text style={[styles.projectStatus, { color: statusColor }]}>
          {project.status}
        </Text>
      </View>
      
      <Text style={styles.projectDescription}>{project.description}</Text>
      
      <View style={styles.projectStats}>
        <View style={styles.stat}>
          <Icon name="account-group" size={16} color="#AAA" />
          <Text style={styles.statText}>{project.participants}</Text>
        </View>
        <View style={styles.stat}>
          <Icon name="flag-checkered" size={16} color="#AAA" />
          <Text style={styles.statText}>{project.milestones}</Text>
        </View>
        <Text style={styles.projectDate}>Created: {project.created_at}</Text>
      </View>
      
      {isSelected && (
        <View style={styles.selectedIndicator}>
          <Text style={styles.selectedText}>Selected</Text>
        </View>
      )}
      
      <TouchableOpacity 
        style={styles.detailsButton}
        onPress={() => onDetails(project.id)}
      >
        <Text style={{ color: theme.colors.primary }}>View Details</Text>
        <Icon name="chevron-right" size={16} color={theme.colors.primary} />
      </TouchableOpacity>
    </TouchableOpacity>
  );
};

// Milestone Card Component
const MilestoneCard = ({ milestone, onPress }: any) => {
  const theme = useTheme();
  
  // Determine status color
  let statusColor = '#AAA';
  if (milestone.status === 'Funded') statusColor = theme.colors.primary;
  if (milestone.status === 'Completed') statusColor = theme.colors.accent;
  if (milestone.status === 'Approved') statusColor = '#00FFA3';
  
  return (
    <TouchableOpacity 
      style={[styles.milestoneCard, { backgroundColor: theme.colors.surface }]}
      onPress={onPress}
    >
      <View style={styles.milestoneHeader}>
        <Text style={styles.milestoneTitle}>{milestone.title}</Text>
        <Text style={[styles.milestoneStatus, { color: statusColor }]}>
          {milestone.status}
        </Text>
      </View>
      
      <Text style={styles.milestoneDescription}>{milestone.description}</Text>
      
      <View style={styles.milestoneDetails}>
        <View style={styles.milestoneDetail}>
          <Icon name="calendar" size={14} color="#AAA" />
          <Text style={styles.detailText}>Deadline: {milestone.deadline}</Text>
        </View>
        <View style={styles.milestoneDetail}>
          <Icon name="cash" size={14} color="#AAA" />
          <Text style={styles.detailText}>Payment: {milestone.payment}</Text>
        </View>
      </View>
      
      {milestone.status === 'Pending' && (
        <Button 
          mode="contained" 
          style={[styles.actionButton, { backgroundColor: theme.colors.primary }]}
          labelStyle={{ fontSize: 12 }}
          onPress={() => {}}
        >
          Fund Milestone
        </Button>
      )}
      
      {milestone.status === 'Funded' && (
        <Button 
          mode="contained" 
          style={[styles.actionButton, { backgroundColor: theme.colors.accent }]}
          labelStyle={{ fontSize: 12 }}
          onPress={() => {}}
        >
          Mark as Completed
        </Button>
      )}
    </TouchableOpacity>
  );
};

// Create Project Form Component
const CreateProjectForm = ({ onSubmit, onCancel }: any) => {
  const theme = useTheme();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [ipTerms, setIpTerms] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const handleSubmit = async () => {
    if (!name || !description) return;
    
    setIsSubmitting(true);
    try {
      await onSubmit({ name, description, ipTerms });
      // Reset form
      setName('');
      setDescription('');
      setIpTerms('');
    } catch (error) {
      console.error('Error creating project:', error);
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <Card style={styles.formCard}>
      <Card.Title title="Create New Project" />
      <Card.Content>
        <TextInput
          label="Project Name"
          value={name}
          onChangeText={setName}
          style={styles.formInput}
          mode="outlined"
        />
        
        <TextInput
          label="Description"
          value={description}
          onChangeText={setDescription}
          style={styles.formInput}
          mode="outlined"
          multiline
          numberOfLines={3}
        />
        
        <TextInput
          label="IP Terms (Optional)"
          value={ipTerms}
          onChangeText={setIpTerms}
          style={styles.formInput}
          mode="outlined"
          multiline
          numberOfLines={3}
          placeholder="Enter intellectual property terms"
        />
        
        <View style={styles.formActions}>
          <Button 
            mode="outlined" 
            onPress={onCancel}
            style={{ marginRight: 8 }}
          >
            Cancel
          </Button>
          <Button 
            mode="contained" 
            onPress={handleSubmit}
            loading={isSubmitting}
            disabled={isSubmitting || !name || !description}
          >
            Create Project
          </Button>
        </View>
      </Card.Content>
    </Card>
  );
};

// Main Screen Component
const SmartContractScreen = () => {
  const theme = useTheme();
  const navigation = useNavigation<StackNavigationProp<any>>();
  const { connected } = useWallet();
  
  const [tabs] = useState(['Explorer', 'Projects', 'Participants']);
  const [activeTab, setActiveTab] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Contract data state
  const [functions, setFunctions] = useState<any[]>([]);
  const [events, setEvents] = useState<any[]>([]);
  
  // Projects state
  const [projects, setProjects] = useState<any[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<string | null>(null);
  const [milestones, setMilestones] = useState<any[]>([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  
  // Load initial data
  useEffect(() => {
    loadContractData();
  }, []);
  
  // Load project milestones when a project is selected
  useEffect(() => {
    if (selectedProjectId) {
      loadProjectMilestones(selectedProjectId);
    } else {
      setMilestones([]);
    }
  }, [selectedProjectId]);
  
  // Load contract data
  const loadContractData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Load contract functions and events
      setFunctions([
        { name: "initialize_project", description: "Creates a new collaboration project" },
        { name: "add_participant", description: "Adds a participant to a project" },
        { name: "add_milestone", description: "Creates a milestone for the project" },
        { name: "fund_milestone_sol", description: "Funds a milestone with SOL" },
        { name: "fund_milestone_usdt", description: "Funds a milestone with USDT stablecoin" },
        { name: "complete_milestone", description: "Marks a milestone as completed" },
        { name: "approve_milestone", description: "Approves a completed milestone" },
        { name: "distribute_milestone_payment", description: "Distributes payment to participants" }
      ]);
      
      setEvents([
        { name: "ProjectCreatedEvent", time: "2025-04-15 14:32:11", transaction: "4ztK...xPq9" },
        { name: "ParticipantAddedEvent", time: "2025-04-15 15:10:22", transaction: "7mnR...vFw2" },
        { name: "MilestoneAddedEvent", time: "2025-04-16 09:45:17", transaction: "2kLp...tR8j" }
      ]);
      
      // Load projects
      const connection = new Connection(clusterApiUrl('devnet'));
      const projectsData = await getProjects(connection);
      setProjects(projectsData);
      
      if (projectsData.length > 0) {
        setSelectedProjectId(projectsData[0].id);
      }
    } catch (err) {
      console.error('Error loading contract data:', err);
      setError('Failed to load contract data. Please try again.');
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };
  
  // Load project milestones
  const loadProjectMilestones = async (projectId: string) => {
    if (!projectId) return;
    
    try {
      const connection = new Connection(clusterApiUrl('devnet'));
      const milestonesData = await getMilestones(connection, projectId);
      setMilestones(milestonesData);
    } catch (err) {
      console.error('Error loading milestones:', err);
    }
  };
  
  // Handle refresh
  const onRefresh = () => {
    setRefreshing(true);
    loadContractData();
  };
  
  // Handle creating a new project
  const handleCreateProject = async (projectData: any) => {
    console.log('Creating project:', projectData);
    // In a real app, this would call your Solana contract
    
    // Refresh projects after creation
    await loadContractData();
    setShowCreateForm(false);
  };
  
  // Handle opening Solana Explorer
  const openExplorer = (path: string) => {
    console.log(`Opening Solana Explorer: ${path}`);
    // In a real app, this would use Linking.openURL
  };
  
  // Handle opening transaction details
  const openTransactionDetails = (signature: string) => {
    navigation.navigate('TransactionDetails', { signature });
  };
  
  // Handle opening project details
  const navigateToProjectDetails = (projectId: string) => {
    navigation.navigate('ProjectDetails', { projectId });
  };
  
  // Handle opening milestone details
  const navigateToMilestoneDetails = (milestoneId: string) => {
    navigation.navigate('MilestoneDetails', { 
      milestoneId, 
      projectId: selectedProjectId 
    });
  };
  
  if (isLoading && !refreshing) {
    return (
      <View style={[styles.container, styles.centered]}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
        <Text style={{ color: theme.colors.text, marginTop: 16 }}>Loading smart contract...</Text>
      </View>
    );
  }

  return (
    <ScrollView 
      style={[styles.container, { backgroundColor: theme.colors.background }]}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Contract Header */}
      <Card style={styles.card}>
        <Card.Content>
          <Text style={styles.contractTitle}>Solana Smart Contract</Text>
          <View style={[styles.contractAddressContainer, { borderLeftColor: theme.colors.primary }]}>
            <Text style={styles.contractAddressLabel}>CONTRACT ADDRESS</Text>
            <Text style={styles.contractAddress}>Coll1ABbXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX</Text>
            <Text style={styles.contractTypeLabel}>CONTRACT TYPE</Text>
            <Text style={styles.contractType}>Collaboration Agreement</Text>
          </View>
        </Card.Content>
      </Card>

      {/* Tabs Navigation */}
      <TabBar
        tabs={tabs}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />

      {/* Explorer Tab */}
      {activeTab === 0 && (
        <View>
          <Card style={styles.card}>
            <Card.Title title="Smart Contract Functions" />
            <Card.Content>
              {functions.map((func, index) => (
                <ContractFunction
                  key={index}
                  name={func.name}
                  description={func.description}
                  onPress={() => openExplorer(`program/Coll1ABbXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX`)}
                />
              ))}
            </Card.Content>
          </Card>

          <Card style={styles.card}>
            <Card.Title title="Contract Events" />
            <Card.Content>
              {events.map((event, index) => (
                <ContractEvent
                  key={index}
                  name={event.name}
                  time={event.time}
                  transaction={event.transaction}
                  onPress={() => openExplorer(`tx/${event.transaction}`)}
                />
              ))}
            </Card.Content>
          </Card>
        </View>
      )}

      {/* Projects Tab */}
      {activeTab === 1 && (
        <View>
          {!showCreateForm ? (
            <>
              <View style={styles.actionBar}>
                <Text style={styles.sectionTitle}>Collaborative Projects</Text>
                <Button 
                  mode="contained" 
                  onPress={() => setShowCreateForm(true)}
                  icon="plus"
                >
                  New Project
                </Button>
              </View>
              
              {projects.length === 0 ? (
                <Card style={styles.emptyCard}>
                  <Card.Content>
                    <Text style={styles.emptyText}>
                      No projects found. Create a new project to get started.
                    </Text>
                  </Card.Content>
                </Card>
              ) : (
                <>
                  {projects.map((project) => (
                    <ProjectCard
                      key={project.id}
                      project={project}
                      isSelected={selectedProjectId === project.id}
                      onSelect={setSelectedProjectId}
                      onDetails={navigateToProjectDetails}
                    />
                  ))}
                  
                  {selectedProjectId && (
                    <Card style={styles.card}>
                      <Card.Title 
                        title="Project Milestones" 
                        right={(props) => (
                          <Button 
                            onPress={() => {}} 
                            mode="text"
                            icon="plus"
                            labelStyle={{ color: theme.colors.primary }}
                          >
                            Add
                          </Button>
                        )}
                      />
                      <Card.Content>
                        {milestones.length === 0 ? (
                          <Text style={styles.emptyText}>
                            No milestones found for this project.
                          </Text>
                        ) : (
                          milestones.map((milestone) => (
                            <MilestoneCard
                              key={milestone.id}
                              milestone={milestone}
                              onPress={() => navigateToMilestoneDetails(milestone.id)}
                            />
                          ))
                        )}
                      </Card.Content>
                    </Card>
                  )}
                </>
              )}
            </>
          ) : (
            <CreateProjectForm
              onSubmit={handleCreateProject}
              onCancel={() => setShowCreateForm(false)}
            />
          )}
        </View>
      )}

      {/* Participants Tab */}
      {activeTab === 2 && (
        <Card style={styles.card}>
          <Card.Title title="Project Participants" />
          <Card.Content>
            <Text style={styles.emptyText}>
              Select a project to manage participants.
            </Text>
          </Card.Content>
        </Card>
      )}

      {/* Connect Wallet Prompt */}
      {!connected && (
        <Card style={[styles.card, styles.walletPrompt]}>
          <Card.Content>
            <View style={styles.walletPromptContent}>
              <Icon name="wallet-outline" size={40} color={theme.colors.primary} />
              <Text style={styles.walletPromptText}>
                Connect a wallet to interact with smart contracts
              </Text>
              <Button 
                mode="contained" 
                onPress={() => navigation.navigate('Account')}
                style={styles.walletButton}
              >
                Connect Wallet
              </Button>
            </View>
          </Card.Content>
        </Card>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  centered: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  card: {
    marginBottom: 16,
    elevation: 4,
  },
  contractTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 16,
    color: '#FFF',
  },
  contractAddressContainer: {
    backgroundColor: '#1E1E1E',
    padding: 16,
    borderRadius: 8,
    borderLeftWidth: 4,
    marginBottom: 8,
  },
  contractAddressLabel: {
    fontSize: 12,
    color: '#AAA',
    marginBottom: 4,
  },
  contractAddress: {
    fontFamily: 'monospace',
    color: '#FFF',
    backgroundColor: '#111',
    padding: 8,
    borderRadius: 4,
    marginBottom: 12,
  },
  contractTypeLabel: {
    fontSize: 12,
    color: '#AAA',
    marginBottom: 4,
  },
  contractType: {
    color: '#FFF',
  },
  tabBar: {
    flexDirection: 'row',
    marginBottom: 16,
    backgroundColor: '#1A1A1A',
    borderRadius: 8,
    padding: 4,
  },
  tab: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 12,
    alignItems: 'center',
    borderRadius: 4,
    borderWidth: 1,
    borderColor: 'transparent',
    margin: 2,
  },
  tabText: {
    color: '#FFF',
    fontWeight: '500',
  },
  contractFunction: {
    backgroundColor: '#1A1A1A',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
    borderLeftWidth: 3,
  },
  functionName: {
    fontFamily: 'monospace',
    fontWeight: 'bold',
    fontSize: 14,
    marginBottom: 4,
  },
  functionDescription: {
    color: '#CCC',
    fontSize: 12,
    marginBottom: 8,
  },
  functionAction: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-end',
  },
  contractEvent: {
    backgroundColor: '#1A1A1A',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
    borderLeftWidth: 3,
  },
  eventHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  eventName: {
    fontFamily: 'monospace',
    fontWeight: 'bold',
    fontSize: 14,
  },
  eventTime: {
    color: '#AAA',
    fontSize: 12,
  },
  eventTransaction: {
    fontFamily: 'monospace',
    color: '#CCC',
    fontSize: 12,
    marginBottom: 8,
  },
  eventAction: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-end',
  },
  actionBar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFF',
  },
  emptyCard: {
    padding: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  emptyText: {
    textAlign: 'center',
    color: '#AAA',
    padding: 16,
  },
  projectCard: {
    padding: 16,
    borderRadius: 8,
    marginBottom: 12,
    borderWidth: 2,
  },
  projectHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  projectTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#FFF',
  },
  projectStatus: {
    fontSize: 12,
    fontWeight: 'bold',
  },
  projectDescription: {
    color: '#CCC',
    marginBottom: 12,
  },
  projectStats: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  stat: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 16,
  },
  statText: {
    color: '#FFF',
    marginLeft: 4,
    fontWeight: 'bold',
  },
  projectDate: {
    color: '#AAA',
    fontSize: 12,
  },
  selectedIndicator: {
    backgroundColor: 'rgba(20, 241, 149, 0.2)',
    paddingVertical: 4,
    paddingHorizontal: 12,
    borderRadius: 16,
    alignSelf: 'flex-start',
    marginTop: 8,
  },
  selectedText: {
    color: '#14F195',
    fontSize: 12,
    fontWeight: 'bold',
  },
  detailsButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-end',
    marginTop: 8,
  },
  milestoneCard: {
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
  },
  milestoneHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  milestoneTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#FFF',
  },
  milestoneStatus: {
    fontSize: 12,
    fontWeight: 'bold',
  },
  milestoneDescription: {
    color: '#CCC',
    fontSize: 12,
    marginBottom: 8,
  },
  milestoneDetails: {
    marginBottom: 8,
  },
  milestoneDetail: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  detailText: {
    color: '#CCC',
    fontSize: 12,
    marginLeft: 4,
  },
  actionButton: {
    borderRadius: 4,
    marginTop: 4,
  },
  formCard: {
    marginBottom: 16,
  },
  formInput: {
    marginBottom: 12,
  },
  formActions: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginTop: 8,
  },
  walletPrompt: {
    backgroundColor: 'rgba(20, 241, 149, 0.1)',
    borderLeftWidth: 3,
    borderLeftColor: '#14F195',
  },
  walletPromptContent: {
    alignItems: 'center',
    padding: 16,
  },
  walletPromptText: {
    textAlign: 'center',
    marginVertical: 16,
    color: '#FFF',
  },
  walletButton: {
    marginTop: 8,
  },
});

export default SmartContractScreen;