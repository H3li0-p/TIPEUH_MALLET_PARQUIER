#include <stdio.h>
#include <stdlib.h>
#include <bool.h>
#include <assert.h>

struct s_cell{
	int val;
	struct s_cell *addr_next;
};

typedef struct s_cell cell;

struct s_stack{
	int siz;
	cell *addr_first;
};

typedef struct s_stack stack;

stack *stack_create()
{
	stack *p = malloc(sizeof(stack));
	if (!p){
		printf("Failed to allocate stack memory\n");
		return NULL;
	}

	p->siz = 0;
	p->addr_first = NULL;

	return p;
}


int stack_length(stack *l)
{
  assert(l != NULL);
  return l->siz;
}

bool stack_is_empty(stack *l)
{
  assert(l != NULL);
  if (l->siz == 0)
    return true;
  return false;
}

int  stack_top(stack *l)
{
  assert(l != NULL);
  cell *c = l->addr_first;

  assert(c != NULL);
  
  return c->val;
}



void stack_push(stack *p,int v)
{
	if (!p){
		printf("Error : trying to push a NULL object\n");
		return;
	}
	cell *first = p->addr_first;
	cell *maillon = malloc(sizeof(cell));
	if (!maillon){
		printf("Allocation failed\n");
		return;
	}
	
	maillon->val = v;
	maillon->addr_next = first;
	p->addr_first = maillon;
	p->siz +=1;

	return;
}

int stack_pop(stack *l)
{
  assert(l != NULL);
  cell *c = l->addr_first;

  assert(c != NULL);
  
  int v = c->val;

  l->addr_first = c->addr_next;
  
  free(c);

  l->siz = l->siz - 1;
  
  return v;
}

void stack_delete(stack *s)
{
 
  assert(s != NULL);
  cell  *c = s->addr_first;
  cell  *tmp = NULL;
  
  while (c != NULL)
  {
    tmp = c;
    c = c->addr_next;
    free(tmp);
  }
  s->addr_first = NULL;
  s->siz = 0;
  return;
}


void stack_free(stack **addr_s)
{
  stack *s = *addr_s;
  assert(s != NULL);
  cell  *c = s->addr_first;
  cell  *tmp = NULL;
  
  while (c != NULL)
  {
    tmp = c;
    c = c->addr_next;
    free(tmp);
  }
  free(s);
  *addr_s = NULL;

  return;
}



int racine_int(int n);

int pgp_rec(int n)
{

}

int plus_grand_premier(int n)//renvoie le plus grand nb premier < 2^n
{
	if (n<1)||(n>31){
		printf("Failed to find prime in range (2 power %d)\n",n);
		return -1;
	}


 
}




int main(int argc,char **argv)
{
	return 0;
}
