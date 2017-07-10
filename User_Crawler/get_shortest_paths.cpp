#include <cstdio>
#include <vector>
#include <queue>
#include <climits>

#define MAXN 1100000
#define MAXD 21

typedef long long LL;

using namespace std;

int N = 0, cnt = 0;

vector<int> g[MAXN];

LL dist[MAXD];

void read_graph() {
    freopen("./data/graph/LSCC_labeled_paths.dat", "r", stdin);
    int src, des, c = 0;
    while (scanf("%d %d", &src, &des) != EOF) {
        ++c;
        if (c % 1000000 == 0)
            printf("%d %d %d\n", c, src, des);
        g[src].push_back(des);
        N = max(N, max(src, des));
    }
    N++;
    for (int i = 0; i < MAXD; i++)
        dist[i] = 0LL;
    printf("-----graph loaded\n");
}

inline void bfs(int src) {
    int d[MAXN];
    bool vis[MAXN];
    for (int i = 0; i < N; i++) {
        d[i] = INT_MAX;
        vis[i] = false;
    }
    queue<int> q;
    q.push(src);
    d[src] = 0;
    vis[src] = true;
    while (!q.empty()) {
        int cur = q.front();
        q.pop();
        for(unsigned int i = 0; i < g[cur].size(); i++) {
            int des = g[cur][i];
            if (!vis[des]) {
                d[des] = d[cur] + 1;
                vis[des] = true;
                q.push(des);
            }
        }
    }
    for (int i = 0; i < N; i++)
        if (d[i] > 0 && d[i] < MAXD)
            ++dist[d[i]];
}

void print_result() {
    freopen("./data/graph/shortest_path.txt", "w", stdout);
    for (int i = 1; i < MAXD; i++)
        printf("%d %lld\n", i, dist[i]);
}

int main() {
    read_graph();

    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < N; i++) {
        if (g[i].size() > 0)
            bfs(i);
        printf("%d/%d\n", ++cnt, N);
        if (cnt % 300 == 0) {
            for (int j = 0; j < MAXD; j++)
                printf("%lld ", dist[j]);
            printf("\n");
        }
    }

    print_result();
    return 0;
}