#include <stdio.h>
#include <stdbool.h>

#define PNAME "CUSTOMER.txt"
#define CNAME "ORDER.txt"

#define NAME_LEN 32

FILE *par;
FILE *cld;

typedef struct header {
	int next_id;
	int next_free;
} ph;

void flush() {
	fpurge(stdin);
}

ph parhdr;
ph cldhdr;

typedef struct tm {
	int id;
	char name[NAME_LEN];
	char address[NAME_LEN];
	int first_child;
} tm;

typedef struct ts {
	int id;
	char name[NAME_LEN];
	int price;
	int count;
	int next_child;
} ts;

void insertm();

void insert_m(tm *item);
bool get_m(int id, tm *item, int *offset);
bool update_m(tm *item);
bool delete_m(int id);

void insert_s(int pid, ts *item);
bool get_s(int pid, int id, ts *item, int *offset, int *prev);
bool update_s(int pid, ts *item);
bool delete_s(int pid, int id);
void stats();



int main() {
	int choice = 1;
	par = fopen(PNAME, "r+");
	cld = fopen(CNAME, "r+");
	setbuf(par, NULL);
	setbuf(cld, NULL);

	do {
		puts("0. EXIT");
		puts("1. INSERT_M");
		puts("2. DELETE_M");
		puts("3. GET_M");
		puts("4. UPDATE_M");
		puts("5. INSERT_S");
		puts("6. DELETE_S");
		puts("7. GET_S");
		puts("8. UPDATE_S");
		puts("9. PRINT");
		puts("10. CLEAN");

		scanf("%d", &choice);
		flush();

		switch (choice) {
		case 0: break;
		case 10: {
				puts("CLEANED!");
				fclose(par);
				fclose(cld);
				par = fopen(PNAME, "w");
				cld = fopen(CNAME, "w");
				setbuf(par, NULL);
				setbuf(cld, NULL);
				parhdr.next_id = cldhdr.next_id = 1;
				parhdr.next_free = cldhdr.next_free = -1;
				fwrite(&parhdr, sizeof(ph), 1, par);
				fwrite(&cldhdr, sizeof(ph), 1, cld);
				break;
			 }
		case 1: insertm(); break;
		case 2: {
				int id;
				printf("ID: ");
				scanf("%d", &id);
				flush();
				printf("Deleted %s\n", delete_m(id) ? "" : "un");
				break;
			}
		case 3: {
				int id;
				tm it;
				int offset;
				printf("ID: ");
				scanf("%d", &id);
				flush();

				if (!get_m(id, &it, &offset)) {
					printf("Id does not exist\n");
					break;
				}
				
				printf("Id: %d, name: %s, address: %s\n", it.id, it.name, it.address);
				break;
			}
		case 4: {
				int id;
				tm it;
				int offset;

				printf("ID: ");
				scanf("%d", &it.id);
				flush();
				printf ("NAME ");
				fgets(it.name, NAME_LEN, stdin);
				flush();
				printf ("ADDRESS: ") ;
				fgets(it.address, NAME_LEN, stdin);
				flush();

				if (update_m(&it))
					printf("Updated!\n");

				break;
			}
		case 5: {
				int pid;
				ts ci;
				printf("CUSTOMER: ");
				scanf("%d", &pid);
				flush();
				printf("NAME: ");
				fgets(ci.name, NAME_LEN, stdin);
				flush();
				printf("PRICE: ");
				scanf("%d", &ci.price);
				flush();
				printf("COUNT: ");
				scanf("%d", &ci.count);
				flush();
				insert_s(pid, &ci);
				printf("New id: %d\n", ci.id);
				break;
			}
		case 6: {
				int pid, id;
				printf("CUSOTMER: ");
				scanf("%d", &pid);
				flush();
				printf("ID:");
				scanf("%d", &id);
				flush();
				printf("Deleted %s!! \n", delete_s(pid, id) ? "" : "un");
				break;
			}
		case 7: {
				int pid, id, offset;
				ts it;
				printf("CUSTOMER ID ");
				scanf("%d", &pid);
				flush();
				printf("ID: ");
				scanf("%d", &id);
				flush();

				if (!get_s(pid, id, &it, &offset, NULL)) {
					printf("NO ID\n");
					break;
				}

				printf("Id: %d, name: %s, price: %d, count: %d\n", it.id, it.name, it.price, it.count);
				break;
			}
		case 8: {
				int pid, id;
				ts ci;
				printf("CUSTOMER ID ");
				scanf("%d", &pid);
				flush();
				printf("ID: ");
				scanf("%d", &ci.id);
				flush();
				printf("NAME: ");
				fgets(ci.name, NAME_LEN, stdin);
				flush();
				printf("PRICE: ");
				scanf("%d", &ci.price);
				flush();
				printf("COUNT: ");
				scanf("%d", &ci.count);
				flush();
				if (update_s(pid, &ci))
					printf("UPDATED!\n");
				break;
			}
		case 9: {
			stats();
			break;
			}

		}
		break;
	} while (choice != 0);
	fclose(par);
	fclose(cld);
}



void insertm() {
	tm s;
	printf ("NAME: ");
	fgets(s.name, NAME_LEN, stdin);
	flush();
	printf ("ADDRESS: ") ;
	fgets(s.address, NAME_LEN, stdin);
	flush();
	insert_m(&s);
	printf("CUSTOMER ID: %d\n", s.id);
}



bool get_m(int id, tm *item, int *offset) {
	int ret;

	fseek(par, sizeof(parhdr), SEEK_SET);

	*offset = sizeof(parhdr);
	do {
		*offset += sizeof(tm);
	} while ((ret = fread(item, sizeof(tm), 1, par)) && item->id != id);
	*offset -= sizeof(tm);

	return !!ret;
}

bool get_s(int pid, int id, ts *item, int *offset, int *prev) {
	int ret;
	tm prnt;

	if (!get_m(pid, &prnt, offset)) {
		printf("NO CUSTOMER WITH THIS ID\n");
		return false;
	}
	
	if (prev) *prev = 0;
	*offset = prnt.first_child;
	while (*offset != 0) {
		fseek(cld, *offset, SEEK_SET);
		if (!fread(item, sizeof(ts), 1, cld))
			return false;
		if (item->id == id)
			return true;
		if (prev) *prev = *offset;
		*offset = item->next_child;
	}
	return false;
}

bool update_m(tm *item) {
	int offset;
	tm it;

	if (!get_m(item->id, &it, &offset)) {
		printf("NO CUSTOMER WITH THIS ID\n");
		return false;
	}

	item->first_child = it.first_child;

	fseek(par, offset, SEEK_SET);
	fwrite(item, sizeof(tm), 1, par);
	return true;
}

bool update_s(int pid, ts *item) {
	ts it;
	int offset;

	if (!get_s(pid, item->id, &it, &offset, NULL)) {
		printf("NO ORDER WITH THIS ID\n");
		return false;
	}

	item->next_child = it.next_child;

	fseek(cld, offset, SEEK_SET);
	fwrite(item, sizeof(ts), 1, cld);
	return true;
}

bool delete_m(int id) {
	int offset;
	tm it;

	if (!get_m(id, &it, &offset)) {
		printf("NO CUSTOMER WITH THIS ID\\n");
		return false;
	}

	while (it.first_child != 0) {
		ts cl;
		fseek(cld, it.first_child, SEEK_SET);
		fread(&cl, 1, sizeof(ts), cld);
		delete_s(id, cl.id);

		fseek(par, offset, SEEK_SET);
		fread(&it, 1, sizeof(tm), par);
	}

	it.id = -1;

	fseek(par, offset, SEEK_SET);
	fwrite(&it, sizeof(tm), 1, par);

	fseek(par, 0, SEEK_SET);
	fread(&parhdr, sizeof(ph), 1, par);

	if (parhdr.next_free < 0 || parhdr.next_free > offset) {
		parhdr.next_free = offset;
		fseek(par, 0, SEEK_SET);
		fwrite(&parhdr, sizeof(ph), 1, par);
	}
	return true;
}

bool delete_s(int pid, int id) {
	tm prnt;
	ts it;
	int offset, prev;
	int poffset;

	if (!get_m(pid, &prnt, &poffset)) {
		printf("NO CUSTOMER WITH THIS ID\n");
		return false;
	}

	if (!get_s(pid, id, &it, &offset, &prev)) {
		printf("NO ORDER WITH THIS ID\n");
		return false;
	}

	if (prnt.first_child == offset) {
		prnt.first_child = it.next_child;
		fseek(par, poffset, SEEK_SET);
		fwrite(&prnt, sizeof(tm), 1, par);
	}

	if (prev != 0) {
		ts pp;
		fseek(cld, prev, SEEK_SET);
		fread(&pp, sizeof(ts), 1, cld);
		pp.next_child = it.next_child;
		fwrite(&pp, sizeof(ts), 1, cld);
	}

	it.id = -1;
	fwrite(&it, sizeof(ts), 1, cld);

	fseek(cld, 0, SEEK_SET);
	fread(&cldhdr, sizeof(ph), 1, cld);

	if (cldhdr.next_free < 0 || cldhdr.next_free > offset) {
		cldhdr.next_free = offset;
		fseek(cld, 0, SEEK_SET);
		fwrite(&cldhdr, sizeof(ph), 1, cld);
	}
	return true;
}

void insert_s(int id, ts *item) {
	int offset;
	tm prnt;

	if (!get_m(id, &prnt, &offset)) {
		printf("NO ORDER WITH THIS ID\n");
		return;
	}

	fseek(cld, 0, SEEK_SET);
	fread(&cldhdr, sizeof(ph), 1, cld);

	if (cldhdr.next_free >= 0) fseek(cld, cldhdr.next_free, SEEK_SET);
	else fseek(cld, 0, SEEK_END);

	item->id = cldhdr.next_id++;
	item->next_child = 0;
	fwrite(item, sizeof(ts), 1, cld);
	int newpos = ftell(cld) - sizeof(ts);

	if (cldhdr.next_free >= 0) {
		ts it;
		int ret;
		do {}
		while ((ret = fread(&it, sizeof(ts), 1, cld)) && it.id != -1);

		cldhdr.next_free = ret ? ftell(par) - sizeof(ts) - sizeof(ph) : -1;
	}


	if (prnt.first_child == 0) {
		prnt.first_child = newpos;;
		fseek(par, offset, SEEK_SET);
		fwrite(&prnt, sizeof(tm), 1, par);
	} else {
		int pos = prnt.first_child;
		ts child;
		child.next_child = pos;
		do {
			pos = child.next_child;
			fseek(cld, pos, SEEK_SET);
			fread(&child, sizeof(ts), 1, cld);
		} while (child.next_child != 0);
		child.next_child = newpos;
		fseek(cld, pos, SEEK_SET);
		fwrite(&child, sizeof(ts), 1, cld);
	}

	fseek(cld, 0, SEEK_SET);
	fwrite(&cldhdr, sizeof(ph), 1, cld);
}

void insert_m(tm *item) {
	fseek(par, 0, SEEK_SET);
	fread(&parhdr, sizeof(ph), 1, par);

	item->first_child = 0;

	if (parhdr.next_free >= 0) fseek(par, parhdr.next_free, SEEK_SET);
	else fseek(par, 0, SEEK_END);

	item->id = parhdr.next_id++;
	fwrite(item, sizeof(tm), 1, par);

	if (parhdr.next_free >= 0) {
		tm it;
		int ret;
		do {}
		while ((ret = fread(&it, sizeof(tm), 1, par)) && it.id != -1);

		parhdr.next_free = ret ? ftell(par) - sizeof(tm) - sizeof(ph) : -1;
	}

	fseek(par, 0, SEEK_SET);
	fwrite(&parhdr, sizeof(ph), 1, par);
}



void stats() {
	int tpc, tcc, ccc;
	tpc = tcc = ccc = 0;

	fseek(par, sizeof(ph), SEEK_SET);
	while (true) {
		tm pa;
		int cldoff;
		if (fread(&pa, sizeof(tm), 1, par) == 0)
			break;
		if (pa.id < 0) continue;

		++tpc;
		ccc = 0;
		cldoff = pa.first_child;
		while (cldoff != 0) {
			ts cl;
			++ccc;
			++tcc;
			fseek(cld, cldoff, SEEK_SET);
			fread(&cl, sizeof(ts), 1, cld);
			cldoff = cl.next_child;
			break;
		}
		printf("CUSTOMER %d: %d ORDER\n", pa.id, ccc);
	}

	printf("TOTAL CUSTOMERS: %d, TOTAL ORDERS: %d\n", tpc, tcc);
}