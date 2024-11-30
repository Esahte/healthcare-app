const API_URL = 'http://localhost:5000/api'

export const healthcareApi = {
    getParameters: async () => {
        try {
            const response = await fetch(`${API_URL}/parameters`)
            if (!response.ok) throw new Error('Network response was not ok')
            return await response.json()
        } catch (error) {
            console.error('Error fetching parameters:', error)
            throw error
        }
    },

    uploadFile: async (file) => {
        try {
            const formData = new FormData()
            formData.append('file', file)

            const response = await fetch(`${API_URL}/upload`, {
                method: 'POST',
                body: formData,
            })
            if (!response.ok) throw new Error('Network response was not ok')
            return await response.json()
        } catch (error) {
            console.error('Error uploading file:', error)
            throw error
        }
    },

    updateParameters: async (params) => {
        try {
            const response = await fetch(`${API_URL}/parameters`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(params),
            })
            if (!response.ok) throw new Error('Network response was not ok')
            return await response.json()
        } catch (error) {
            console.error('Error updating parameters:', error)
            throw error
        }
    },

    getAllocations: async (clusterData, riskLevels) => {
        try {
            const response = await fetch(`${API_URL}/allocate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    cluster_data: clusterData,
                    risk_levels: riskLevels,
                }),
            })
            if (!response.ok) throw new Error('Network response was not ok')
            return await response.json()
        } catch (error) {
            console.error('Error getting allocations:', error)
            throw error
        }
    }
}