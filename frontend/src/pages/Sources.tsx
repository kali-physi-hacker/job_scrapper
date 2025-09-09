import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useToast } from '@/components/ui/toast'

type Source = { id: number; key: string; base_url: string; enabled: boolean }

export default function Sources() {
  const [sources, setSources] = useState<Source[]>([])
  const [form, setForm] = useState({ key: 'greenhouse', base_url: '' })
  const [loading, setLoading] = useState(false)
  const [bulkText, setBulkText] = useState('')
  const [discoverText, setDiscoverText] = useState('')
  const { add } = useToast()

  const load = async () => {
    const { data } = await api.get('/jobs/sources/')
    setSources(data?.results ?? data)
  }

  useEffect(() => { load() }, [])

  const createSource = async () => {
    if (!form.base_url) return
    setLoading(true)
    try {
      await api.post('/jobs/sources/', { key: form.key, base_url: form.base_url, enabled: true })
      setForm({ key: 'greenhouse', base_url: '' })
      await load()
    } finally { setLoading(false) }
  }

  const crawl = async (id: number) => {
    await api.post(`/jobs/sources/${id}/crawl/`, { query: '', location: '' })
  }

  const bulkAdd = async () => {
    const urls = bulkText.split('\n').map(s => s.trim()).filter(Boolean)
    if (!urls.length) return
    setLoading(true)
    try {
      await api.post('/jobs/sources/bulk/', { urls })
      setBulkText('')
      await load()
    } finally { setLoading(false) }
  }

  const discover = async () => {
    const slugs = discoverText.split('\n').map(s => s.trim()).filter(Boolean)
    if (!slugs.length) return
    setLoading(true)
    try {
      const { data } = await api.post('/jobs/sources/discover/', { slugs, concurrency: 30 })
      add({ title: 'Discovery queued', description: `Task ${data.task_id}` })
      setDiscoverText('')
    } finally { setLoading(false) }
  }

  return (
    <div className="grid gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Add Source</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 sm:grid-cols-3">
            <div>
              <Label htmlFor="key">Key</Label>
              <select id="key" className="mt-1 w-full h-9 rounded-md border border-input bg-transparent px-3 text-sm"
                value={form.key} onChange={e => setForm(s => ({ ...s, key: e.target.value }))}>
                <option value="greenhouse">greenhouse</option>
                <option value="lever">lever</option>
              </select>
            </div>
            <div className="sm:col-span-2">
              <Label htmlFor="base">Base URL</Label>
              <Input id="base" placeholder="https://boards.greenhouse.io/<company>" value={form.base_url} onChange={e => setForm(s => ({ ...s, base_url: e.target.value }))} />
            </div>
          </div>
          <div className="mt-4">
            <Button onClick={createSource} disabled={loading}>Save Source</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Bulk Add Sources</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-2">
            <Label htmlFor="bulk">Paste career board URLs (one per line)</Label>
            <textarea id="bulk" className="min-h-[140px] rounded-md border border-input bg-transparent px-3 py-2 text-sm" value={bulkText} onChange={e => setBulkText(e.target.value)} />
            <div>
              <Button onClick={bulkAdd} disabled={loading}>Bulk Add</Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Discover by Company Slugs</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-2">
            <Label htmlFor="discover">Paste company slugs (e.g., stripe, notion, figma)</Label>
            <textarea id="discover" className="min-h-[140px] rounded-md border border-input bg-transparent px-3 py-2 text-sm" value={discoverText} onChange={e => setDiscoverText(e.target.value)} />
            <div>
              <Button onClick={discover} disabled={loading}>Discover</Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Sources</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="divide-y">
            {sources.map(s => (
              <div key={s.id} className="flex items-center justify-between py-3">
                <div>
                  <div className="font-medium">{s.key}</div>
                  <div className="text-sm text-muted-foreground truncate max-w-xl">{s.base_url}</div>
                </div>
                <div className="flex items-center gap-2">
                  <Button variant="secondary" onClick={() => crawl(s.id)}>Crawl</Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
