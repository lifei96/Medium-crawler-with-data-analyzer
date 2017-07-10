#include <pthread.h>
#include <cstdio>
#include <cstring>
#include <vector>
#include <algorithm>

using namespace std;

#define NTHREAD 12ll
typedef long long ll;

const int maxn = 1100000; // Number of nodes
vector<int> V[maxn];
vector<int> V2[maxn];
unsigned int f[NTHREAD * maxn];
int d[maxn];
int n;
bool vis[NTHREAD * maxn];

int Gint() {
	char ch;
	while (ch = getchar(), !('0' <= ch && ch <= '9'));
	int ret = ch - 48;
	while (ch = getchar(), ('0' <= ch && ch <= '9')) ret = ret * 10 + ch - 48;
	return ret;
}

void readData() {
	int id;
	while (~scanf("%d", &id)) {
        fprintf(stderr, "nowid = %d\n", id);
        ++id;
		//if ((id & 65535) == 65535) {
		//	fprintf(stderr, "nowid = %d\n", id);
		//}
		int y, x = Gint();
		while (x--) {
			y = Gint();
            ++y;
			V[id].push_back(y);
			V[y].push_back(id);
			V2[id].push_back(y);
		}
	}
    fprintf(stderr, "readed\n");
	n = id;
	for (int i = 1; i <= n; ++i) {
		sort(V[i].begin(), V[i].end());
		auto it = unique(V[i].begin(), V[i].end());
		V[i].resize(distance(V[i].begin(), it));
		d[i] = V[i].size();
	}
}

void* process(void *arg) {
	int no = *(int*)arg;
	int start, end;
	start = (n / NTHREAD + 1) * no + 1;
	end = start + (n / NTHREAD + 1) - 1;
	if (end > n) end = n;
	size_t base = (size_t)no * maxn;

	for (int id = start; id <= end; ++id) {
		if ((id & 65535) == 65535) {
			fprintf(stderr, "nowid = %d\n", id);
		}
		for (const auto &i : V[id]) {
			vis[base + i] = true;
		}
		for (const auto &y : V2[id]) {
			for (const auto &z : V[y]) {
				f[base + z] += vis[base + z];
			}
		}
		for (const auto &i : V[id]) {
			vis[base + i] = false;
		}
	}
	char name[40];
	sprintf(name, "aaaannnnssss%d.txt", no);
	FILE *fp = fopen(name, "w");
	for (int i = 1; i <= n; i++) {
		fprintf(fp, "%d %u %d\n", i, f[base + i], d[i]);
		//if (d[i] <= 1) fprintf(fp, "%d %.6f\n", i, 0.0);
		//else fprintf(fp, "%d %.6f\n", i, f[i] / (1.0 * d[i] * (d[i] - 1))); //d[i] <= 1?
	}
	fclose(fp);
	
	return ((void *)0);
}

void merge() {
	FILE *fp = fopen("./data/graph/CC.txt", "w");
	for (size_t i = 1; i <= (size_t)n; i++) {
		for (size_t j = 1; j < NTHREAD; j++) {
			f[i] += f[i + j * maxn];
		}
	}
	for (int i = 1; i <= n; i++) {
		if (d[i] <= 1) {
			fprintf(fp, "%d %.6f\n", i - 1, 0.0);
		} else {
			fprintf(fp, "%d %.6f\n", i - 1, f[i] / (1.0 * d[i] * (d[i] - 1)));
		}
	}
}


int main() {
	freopen("./data/graph/graph_labeled_CC.dat", "r", stdin);
    fprintf(stderr, "freopened\n");
	pthread_t tid[NTHREAD];
    fprintf(stderr, "pthread\n");
	readData();
    fprintf(stderr, "inited\n");
	int tname[NTHREAD];
	for (int i = 0; i < NTHREAD; i++) {
		tname[i] = i;
		int err = pthread_create(&tid[i], NULL, process, &tname[i]);
		if (err != 0) {
			fprintf(stderr, "Can't create thread\n");
			return 0;
		}
        fprintf(stderr, "Thread %d created\n", i);
	}
	for (int i = 0; i < NTHREAD; i++) {
		pthread_join(tid[i], NULL);
	}
	merge();
	return 0;
}
