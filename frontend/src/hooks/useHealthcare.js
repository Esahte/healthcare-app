import {useEffect, useState} from 'react'
import {healthcareApi} from '../services/api'

export function useHealthcare() {
    const [activeTab, setActiveTab] = useState('upload')
    const [loading, setLoading] = useState(false)
    const [resourceParams, setResourceParams] = useState({})
    const [results, setResults] = useState(null)
    const [error, setError] = useState(null)

    useEffect(() => {
        loadParameters()
    }, [])

    const loadParameters = async () => {
        try {
            const params = await healthcareApi.getParameters()
            setResourceParams(params)
        } catch (err) {
            setError('Failed to load parameters')
            console.error('Error loading parameters:', err)
        }
    }

    const handleFileUpload = async (event) => {
        if (!event.target.files?.[0]) return

        setLoading(true)
        try {
            const result = await healthcareApi.uploadFile(event.target.files[0])
            setResults(result)
            setActiveTab('results')
        } catch (err) {
            setError('Failed to process file')
            console.error('Error uploading file:', err)
        } finally {
            setLoading(false)
        }
    }

    const handleParameterUpdate = async () => {
        try {
            await healthcareApi.updateParameters(resourceParams)

            if (results) {
                const newResults = await healthcareApi.getAllocations(
                    results.cluster_data,
                    results.risk_levels
                )
                setResults(newResults)
            }
        } catch (err) {
            setError('Failed to update parameters')
            console.error('Error updating parameters:', err)
        }
    }

    const handleResourceParamChange = (resource, value) => {
        setResourceParams(prev => ({
            ...prev,
            [resource]: parseInt(value) || 0
        }))
    }

    return {
        activeTab,
        setActiveTab,
        loading,
        resourceParams,
        results,
        error,
        handleFileUpload,
        handleParameterUpdate,
        handleResourceParamChange
    }
}