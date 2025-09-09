import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

type Job = {
  id: number
  title: string
  location: string
  remote: boolean
  description_text: string
  company?: { name: string }
}

type Prepared = { [jobId: number]: number } // jobId -> applicationId

export default function Jobs() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(false)
  const [scores, setScores] = useState<Record<number, number>>({})
  const [prepared, setPrepared] = useState<Prepared>({})
  const [filters, setFilters] = useState({ q: '', location: '', remote: 'any', min_score: 0 })
  const [resumes, setResumes] = useState<{ id: number; title: string }[]>([])
  const [defaultResumeId, setDefaultResumeId] = useState<number | ''>('')

  const load = async () => {
    setLoading(true)
    try {
      const { data } = await api.get('/jobs/postings/')
      const arr = data?.results ?? data
      setJobs(arr)
    } finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])
  useEffect(() => { (async () => {
    const { data } = await api.get('/core/documents/?kind=resume')
    const arr = data?.results ?? data
    setResumes(arr.map((d: any) => ({ id: d.id, title: d.title })))
  })() }, [])

  const scoreAll = async () => {
    await api.post('/jobs/postings/score-all/')
  }

  const scoreOne = async (id: number) => {
    const { data } = await api.get(`/jobs/postings/${id}/my-score/`)
    setScores(s => ({ ...s, [id]: data.score }))
  }

  const prepareApply = async (id: number) => {
    const { data } = await api.post('/applications/applications/prepare/', { job_id: id, resume_id: defaultResumeId || undefined })
    setPrepared(p => ({ ...p, [id]: data.id }))
  }

  const tailorCover = async (jobId: number) => {
    const appId = prepared[jobId]
    if (!appId) return
    await api.post(`/applications/applications/${appId}/tailor-cover/`, { tone: 'professional' })
  }

  const fetchTopMatches = async () => {
    const params = new URLSearchParams()
    if (filters.q) params.set('q', filters.q)
    if (filters.location) params.set('location', filters.location)
    if (filters.remote !== 'any') params.set('remote', filters.remote)
    if (filters.min_score) params.set('min_score', String(filters.min_score))
    const { data } = await api.get(`/jobs/postings/top-matches/?${params.toString()}`)
    setJobs(data)
    const map: Record<number, number> = {}
    data.forEach((j: any) => { if (j._score != null) map[j.id] = j._score })
    setScores(map)
  }

  return (
    <div className="grid gap-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Jobs</h2>
        <div className="flex items-center gap-2">
          <Button onClick={scoreAll} variant="secondary">Score All</Button>
          <Button onClick={fetchTopMatches}>Top Matches</Button>
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
        <input placeholder="Search title" className="h-9 rounded-md border border-input bg-transparent px-3 text-sm"
               value={filters.q} onChange={e => setFilters(f => ({ ...f, q: e.target.value }))}/>
        <input placeholder="Location" className="h-9 rounded-md border border-input bg-transparent px-3 text-sm"
               value={filters.location} onChange={e => setFilters(f => ({ ...f, location: e.target.value }))}/>
        <select className="h-9 rounded-md border border-input bg-transparent px-3 text-sm"
                value={filters.remote} onChange={e => setFilters(f => ({ ...f, remote: e.target.value }))}>
          <option value="any">Any</option>
          <option value="true">Remote</option>
          <option value="false">Onsite</option>
        </select>
        <input type="number" min={0} max={1} step={0.05} placeholder="Min score (0-1)" className="h-9 rounded-md border border-input bg-transparent px-3 text-sm"
               value={filters.min_score} onChange={e => setFilters(f => ({ ...f, min_score: Number(e.target.value) }))}/>
      </div>
      <div className="flex items-center gap-3">
        <label className="text-sm text-muted-foreground">Default Resume</label>
        <select className="h-9 rounded-md border border-input bg-transparent px-3 text-sm" value={defaultResumeId}
                onChange={e => setDefaultResumeId(e.target.value ? Number(e.target.value) : '')}>
          <option value="">None</option>
          {resumes.map(r => <option key={r.id} value={r.id}>{r.title}</option>)}
        </select>
      </div>
      <div className="grid gap-4">
        {jobs.map(j => (
          <Card key={j.id}>
            <CardHeader>
              <CardTitle className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                <span>{j.title} {j.company?.name ? `· ${j.company.name}` : ''}</span>
                <span className="text-sm text-muted-foreground flex items-center gap-3">
                  {scores[j.id] != null && <span className="inline-flex items-center rounded-full bg-secondary px-2 py-0.5 text-xs">Score {(scores[j.id]*100).toFixed(0)}%</span>}
                  {j.location || (j.remote ? 'Remote' : '')}
                </span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="prose prose-sm max-w-none line-clamp-3 text-muted-foreground">
                {j.description_text}
              </div>
              <div className="mt-4 flex items-center gap-2">
                <Button onClick={() => scoreOne(j.id)}>My Score {scores[j.id] != null ? `(${(scores[j.id]*100).toFixed(0)}%)` : ''}</Button>
                <Button variant="outline" onClick={() => prepareApply(j.id)}>Prepare Apply</Button>
                {prepared[j.id] && <Button variant="secondary" onClick={() => tailorCover(j.id)}>Tailor Cover</Button>}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
