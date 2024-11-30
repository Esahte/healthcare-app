import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from 'recharts'
import {Activity, FileUp, Settings} from 'lucide-react'
import {useHealthcare} from '../../hooks/useHealthcare'

const UploadTab = ({handleFileUpload, loading}) => (
    <div className="space-y-6">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center bg-white">
            <FileUp className="mx-auto h-12 w-12 text-gray-400"/>
            <p className="mt-2 text-sm text-gray-600">
                Upload patient data CSV file
            </p>
            <input
                type="file"
                accept=".csv"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
            />
            <label
                htmlFor="file-upload"
                className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg cursor-pointer inline-block hover:bg-blue-600"
            >
                Select File
            </label>
        </div>
        {loading && <p className="text-center text-gray-700">Processing data...</p>}
    </div>
)

const ParametersTab = ({resourceParams, handleResourceParamChange, handleParameterUpdate}) => (
    <div className="space-y-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800">Resource Availability</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(resourceParams).map(([resource, value]) => (
                <div key={resource} className="space-y-2">
                    <label className="text-sm font-medium text-gray-700">
                        {resource.replace(/_/g, ' ')}
                    </label>
                    <input
                        type="number"
                        value={value}
                        onChange={(e) => handleResourceParamChange(resource, e.target.value)}
                        className="w-full p-2 border rounded-lg bg-white text-gray-800"
                    />
                </div>
            ))}
        </div>
        <button
            onClick={handleParameterUpdate}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
            Update Parameters
        </button>
    </div>
)

const ResultsTab = ({results}) => (
    results && (
        <div className="space-y-8">
            <div>
                <h2 className="text-xl font-semibold mb-4 text-gray-800">Cluster Analysis</h2>
                <div className="overflow-x-auto">
                    <table className="min-w-full bg-white">
                        <thead>
                        <tr className="bg-gray-50">
                            <th className="p-3 text-left text-gray-700">Cluster</th>
                            <th className="p-3 text-left text-gray-700">Risk Level</th>
                            <th className="p-3 text-right text-gray-700">Number of Patients</th>
                        </tr>
                        </thead>
                        <tbody>
                        {Object.entries(results.cluster_risks).map(([cluster, risk]) => (
                            <tr key={cluster} className="border-t">
                                <td className="p-3 text-gray-800">Cluster {cluster}</td>
                                <td className="p-3 text-gray-800">{risk}</td>
                                <td className="p-3 text-right text-gray-800">
                                    {Math.floor(Math.random() * 100) + 50}
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <div>
                <h2 className="text-xl font-semibold mb-4 text-gray-800">Resource Allocation Visualization</h2>
                <div className="h-64 bg-white p-4 rounded-lg">
                    <BarChart
                        width={800}
                        height={250}
                        data={Object.entries(results.cluster_risks).map(([cluster, risk]) => ({
                            cluster: `Cluster ${cluster}`,
                            risk: risk,
                            allocated: Math.floor(Math.random() * 100),
                            demanded: Math.floor(Math.random() * 150)
                        }))}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="cluster"/>
                        <YAxis/>
                        <Tooltip/>
                        <Legend/>
                        <Bar dataKey="demanded" fill="#8884d8" name="Demanded"/>
                        <Bar dataKey="allocated" fill="#82ca9d" name="Allocated"/>
                    </BarChart>
                </div>
            </div>
        </div>
    )
)

export default function HealthcareDashboard() {
    const {
        activeTab,
        setActiveTab,
        loading,
        resourceParams,
        results,
        error,
        handleFileUpload,
        handleParameterUpdate,
        handleResourceParamChange
    } = useHealthcare()

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="max-w-7xl mx-auto px-4 py-6">
                <h1 className="text-3xl font-bold mb-8 text-gray-800">Healthcare Resource Allocation Dashboard</h1>

                <div className="flex space-x-4 mb-6">
                    <button
                        onClick={() => setActiveTab('upload')}
                        className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                            activeTab === 'upload'
                                ? 'bg-blue-500 text-white'
                                : 'bg-white text-gray-700 hover:bg-gray-100'
                        }`}
                    >
                        <FileUp className="w-4 h-4 mr-2"/>
                        Data Upload
                    </button>
                    <button
                        onClick={() => setActiveTab('parameters')}
                        className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                            activeTab === 'parameters'
                                ? 'bg-blue-500 text-white'
                                : 'bg-white text-gray-700 hover:bg-gray-100'
                        }`}
                    >
                        <Settings className="w-4 h-4 mr-2"/>
                        Parameters
                    </button>
                    <button
                        onClick={() => setActiveTab('results')}
                        className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                            activeTab === 'results'
                                ? 'bg-blue-500 text-white'
                                : 'bg-white text-gray-700 hover:bg-gray-100'
                        }`}
                    >
                        <Activity className="w-4 h-4 mr-2"/>
                        Results
                    </button>
                </div>

                <div className="bg-white rounded-lg shadow-lg p-6">
                    {error && (
                        <div className="bg-red-50 text-red-500 p-4 mb-4 rounded-lg">
                            {error}
                        </div>
                    )}

                    {activeTab === 'upload' && <UploadTab handleFileUpload={handleFileUpload} loading={loading}/>}
                    {activeTab === 'parameters' && (
                        <ParametersTab
                            resourceParams={resourceParams}
                            handleResourceParamChange={handleResourceParamChange}
                            handleParameterUpdate={handleParameterUpdate}
                        />
                    )}
                    {activeTab === 'results' && <ResultsTab results={results}/>}
                </div>
            </div>
        </div>
    )
}