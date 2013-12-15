//
//  ViewController.m
//  BartendroPad
//
//  Created by Pablo Castro on 12/3/13.
//  Copyright (c) 2013 witty. All rights reserved.
//

#import "DrinkListViewController.h"

@interface DrinkListViewController () < UITextFieldDelegate,
                                        UICollectionViewDataSource,
                                        UICollectionViewDelegateFlowLayout>

@property (strong, nonatomic) NSMutableArray * drinkList;
@property (strong, nonatomic) IBOutlet UICollectionView * DrinksMenu;

@end

@implementation DrinkListViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
    
    AFHTTPRequestOperationManager * manager = [AFHTTPRequestOperationManager manager];
    
    [manager GET:@"http://localhost:8080/ws/drink/dindex"
      parameters:nil
     
         success:^(AFHTTPRequestOperation *operation, id responseObject) {
             //NSLog(@"JSON: %@", responseObject);
             
             
             NSArray * l = [responseObject objectForKey:@"DrinkList"];
             //[self fillDrinkListFromJSON:l];
             
         }
     
         failure:^(AFHTTPRequestOperation *operation, NSError *error) {
             NSLog(@"Error: %@", error);
         }
     ];
}


- (void) fillDrinkListFromJSON:(NSArray *) jsonList{

    
    self.drinkList = [[NSMutableArray alloc] init];
    
    for (NSDictionary * dict in jsonList){
        
        //NSLog(@"dict: %@", dict);
        
        Drink * d = [[Drink alloc] init];
        [d fillWithAttributes:dict];
        [self.drinkList addObject:d];
    }
    
    NSLog(@"We have %d drinks", [self.drinkList count]);
    [self.DrinksMenu reloadData];
    
}


- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - UICollectionView Datasource


- (NSInteger)collectionView:(UICollectionView *)view numberOfItemsInSection:(NSInteger)section {
//    NSString *searchTerm = self.searches[section];
//    return [self.searchResults[searchTerm] count];
    
    return [self.drinkList count];
    
}

- (NSInteger)numberOfSectionsInCollectionView: (UICollectionView *)collectionView {
//    return [self.searches count];

    return 1;
}

- (UICollectionViewCell *)collectionView:(UICollectionView *)cv
                  cellForItemAtIndexPath:(NSIndexPath *)indexPath {
    
    DrinkCollectionViewCell * cell = [cv dequeueReusableCellWithReuseIdentifier:@"DrinkCell"
                                                               forIndexPath:indexPath];
    
    Drink * d = [self.drinkList objectAtIndex:indexPath.row];
    
    
    cell.backgroundColor = [UIColor whiteColor];
    cell.drinkDescription.text = d.desc;
    
    return cell;
}


//- (UICollectionReusableView *)collectionView:
// (UICollectionView *)collectionView viewForSupplementaryElementOfKind:(NSString *)kind atIndexPath:(NSIndexPath *)indexPath
// {
// return [[UICollectionReusableView alloc] init];
//}


#pragma mark - UICollectionViewDelegate

- (void)collectionView:(UICollectionView *)collectionView didSelectItemAtIndexPath:(NSIndexPath *)indexPath
{
    // TODO: Select Item
}

- (void)collectionView:(UICollectionView *)collectionView didDeselectItemAtIndexPath:(NSIndexPath *)indexPath {
    // TODO: Deselect item
}















@end
