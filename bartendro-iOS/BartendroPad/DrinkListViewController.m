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

@property (strong, nonatomic) NSMutableArray * topDrinkList;
@property (strong, nonatomic) NSMutableArray * otherDrinkList;

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
             
             NSArray * td = [[[responseObject objectForKey:@"AllDrinks"] objectAtIndex:0] objectForKey:@"topDrinks"];
             NSArray * od = [[[responseObject objectForKey:@"AllDrinks"] objectAtIndex:1] objectForKey:@"otherDrinks"];
             
//             NSLog(@"top drinks  : %@", td);
//             NSLog(@"Other drinks  : %@", td);
             
             
             [self fillTopDrinkListFromJSON:td];
             [self fillOtherDrinkListFromJSON:od];
             
             
         }
     
         failure:^(AFHTTPRequestOperation *operation, NSError *error) {
             NSLog(@"Error: %@", error);
         }
     ];
}


- (void) fillTopDrinkListFromJSON:(NSArray *) jsonList{

    self.topDrinkList = [[NSMutableArray alloc] init];
    
    for (NSDictionary * dict in jsonList){
        
        //NSLog(@"dict: %@", dict);
        
        Drink * d = [[Drink alloc] init];
        [d fillWithAttributes:dict];
        [self.topDrinkList addObject:d];
    }
    
    NSLog(@"We have %d Top drinks", [self.topDrinkList count]);
    [self.DrinksMenu reloadData];
    
}


- (void) fillOtherDrinkListFromJSON:(NSArray *) jsonList{
    
    
    self.otherDrinkList = [[NSMutableArray alloc] init];
    
    for (NSDictionary * dict in jsonList){
        
        //NSLog(@"dict: %@", dict);
        
        Drink * d = [[Drink alloc] init];
        [d fillWithAttributes:dict];
        [self.otherDrinkList addObject:d];
    }
    
    NSLog(@"We have %d other drinks", [self.otherDrinkList count]);
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
    
    return [self.topDrinkList count];
    
}

- (NSInteger)numberOfSectionsInCollectionView: (UICollectionView *)collectionView {
//    return [self.searches count];

    return 1;
}

- (UICollectionViewCell *)collectionView:(UICollectionView *)cv
                  cellForItemAtIndexPath:(NSIndexPath *)indexPath {
    
    DrinkCollectionViewCell * cell = [cv dequeueReusableCellWithReuseIdentifier:@"DrinkCell"
                                                               forIndexPath:indexPath];
    
    Drink * d = [self.topDrinkList objectAtIndex:indexPath.row];
    
    
    cell.backgroundColor = [UIColor whiteColor];
    cell.drinkDescription.text = d.desc;
    cell.drinkName.text = d.name;

    
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
