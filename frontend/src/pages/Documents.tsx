import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

type Doc = { id: number; title: string; kind: string; ats_score: number; metadata?: any }

export default function Documents() {
  const [docs, setDocs] = useState<Doc[]>([])
  const [title, setTitle] = useState('My Resume')
  const [file, setFile] = useState<File | null>(null)
  const [keywords, setKeywords] = useState('python, django, react')
  const [loading, setLoading] = useState(false)

  const load = async () => {
    const { data } = await api.get('/core/documents/')
    setDocs(data?.results ?? data)
  }

  useEffect(() => { load() }, [])

  const upload = async () => {
    if (!file) return
    setLoading(true)
    try {
      const form = new FormData()
      form.append('kind', 'resume')
      form.append('title', title)
      form.append('file', file)
      const md = { keywords: keywords.split(',').map(s => s.trim()).filter(Boolean) }
      form.append('metadata', JSON.stringify(md))
      await api.post('/core/documents/', form, { headers: { 'Content-Type': 'multipart/form-data' } })
      setFile(null)
      await load()
    } finally { setLoading(false) }
  }

  return (
    <div className="grid gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Upload Resume</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <Label htmlFor="title">Title</Label>
              <Input id="title" value={title} onChange={e => setTitle(e.target.value)} />
            </div>
            <div>
              <Label htmlFor="file">File</Label>
              <Input id="file" type="file" onChange={e => setFile(e.target.files?.[0] ?? null)} />
            </div>
            <div className="sm:col-span-2">
              <Label htmlFor="keywords">Keywords</Label>
              <Input id="keywords" value={keywords} onChange={e => setKeywords(e.target.value)} placeholder="comma-separated" />
            </div>
          </div>
          <div className="mt-4">
            <Button onClick={upload} disabled={loading || !file}>Upload</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Your Documents</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="divide-y">
            {docs.map(d => (
              <div key={d.id} className="py-3 flex items-center justify-between">
                <div>
                  <div className="font-medium">{d.title} <span className="text-muted-foreground">({d.kind})</span></div>
                  <div className="text-xs text-muted-foreground">Keywords: {Array.isArray(d.metadata?.keywords) ? d.metadata.keywords.join(', ') : '—'}</div>
                </div>
                <div className="text-xs text-muted-foreground">ATS score: {d.ats_score?.toFixed?.(2) ?? 0}</div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

